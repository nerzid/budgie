from logging import PlaceHolder
from flask import request
from torch import ne
from socialds.action.actions.physical.calmdown import CalmDown
from socialds.action.actions.physical.worry import Worry
from socialds.action.actions.verbal.bye import Bye
from socialds.action.actions.verbal.request_confirmation import (
    RequestConfirmation,
    Affirm,
    Deny,
)
from socialds.action.effects.functional.change_place import ChangePlace
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent_placeholder import AgentPlaceholder
from socialds.any import any_information
from socialds.any.any_information import AnyInformation
from socialds.conditions.has_permit import HasPermit
from socialds.conditions.session_status_is import SessionStatusIs
from socialds.expectation_step import ExpectationStep
from socialds.managers.dialogue_manager import DialogueManager
from socialds.managers.session_manager import SessionManager
from socialds.placeholder import Placeholder
from socialds.requirement import Requirement
from socialds.action.action_obj import ActionObjType
from socialds.action.actionoperators.op_and import And
from socialds.action.actionoperators.op_or import Or
from socialds.action.actionoperators.then import Then
from socialds.action.actionoperators.when import When
from socialds.action.actions.mental.deduce import Deduce
from socialds.action.actions.mental.feel import Feel
from socialds.action.actions.physical.examine import Examine
from socialds.action.actions.physical.heal import Heal
from socialds.action.actions.physical.move import Move
from socialds.action.actions.physical.open import Open
from socialds.action.actions.physical.prescribe import Prescribe
from socialds.action.actions.physical.sleep import Sleep
from socialds.action.actions.physical.take import Take
from socialds.action.actions.verbal.acknowledge import Acknowledge
from socialds.action.actions.verbal.request_info import RequestInfo
from socialds.action.actions.verbal.backchannel import Backchannel
from socialds.action.actions.verbal.check import Check
from socialds.action.actions.verbal.greet import Greet
from socialds.action.actions.verbal.have import Have
from socialds.action.actions.verbal.learn import Learn
from socialds.action.actions.verbal.notify import Notify
from socialds.action.actions.verbal.request_action import RequestAction
from socialds.action.actions.verbal.selftalk import SelfTalk
from socialds.action.actions.verbal.share import Share
from socialds.action.actions.verbal.thank import Thank
from socialds.action.actiontimes.after import After
from socialds.action.actiontimes.before import Before
from socialds.action.actiontimes.in_morning import InMorning
from socialds.action.actiontimes.in_week import InWeek
from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.effects.functional.add_expected_effect import AddExpectedEffect
from socialds.action.effects.social.demote_value import DemoteValue
from socialds.action.effects.social.permit import Permit
from socialds.action.effects.social.promote_value import PromoteValue
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.any.any_action import AnyAction
from socialds.any.any_agent import AnyAgent
from socialds.any.any_effect import AnyEffect
from socialds.any.any_place import AnyPlace
from socialds.any.any_property import AnyProperty
from socialds.any.any_relation import AnyRelation
from socialds.any.any_resource import AnyResource
from socialds.conditions.action_on_property_happens import ActionOnResourceHappens
from socialds.conditions.agent_at_place import AgentAtPlace
from socialds.conditions.agent_can_do import AgentCanDo
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.conditions.agent_knows import AgentKnows
from socialds.conditions.expectation_status_is import ExpectationStatusIs
from socialds.enums import PlaceholderSymbol, Tense
from socialds.expectation import ExpectationStatus
from socialds.goal import Goal
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RelationStorage, RSType
from socialds.scenarios.scenario import Scenario
from socialds.session import Session, SessionStatus
from socialds.socialpractice.activity.competence import Competence
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.information import Information
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.context.resource import Resource
from socialds.socialpractice.expectation.norm import Norm
from socialds.states.property import Property
from socialds.states.relation import Relation, RType, Negation
from socialds.states.value import Value
from socialds.utterance import Utterance

SP_NAME = "Eye Dialogue"


def sp_main(data):
    # Globals
    any_agent = AnyAgent()
    any_place = AnyPlace()

    actor_patient = Actor(
        name="Joe", knowledgebase=RelationStorage("Actor Joe's Knowledgebase")
    )

    places = []
    properties = []
    resources = []

    p_patients_name = None
    r_left_eye = None
    r_right_eye = None
    r_both_eyes = None
    p_age_group = None

    r_eye = Resource('eye')
    symptoms = data['symptoms']
    infos_symptom = []
    for symptom in symptoms:
        infos_symptom.append(Information(left=r_eye, rtype=RType.HAS, rtense=Tense.PRESENT, right=Property(symptom)))



    p_what_happened = Property(data['what_happened'])
    history_questions = data['history_questions']
    p_is_first_time = Property(history_questions['is_first_time'])
    p_when_happened = Property(history_questions['when_happened'])
    p_has_contact_lenses = Property(history_questions['has_contact_lenses'])
    p_did_self_cure = Property(history_questions['did_self_cure'])
    p_did_take_drugs = Property(history_questions['did_take_drugs'])
    p_has_allergy = Property(history_questions['has_allergy'])
    p_has_rheumatic_disease = Property(history_questions['has_rheumatic_disease'])
    p_does_relatives_have_it = Property(history_questions['does_relatives_have_it'])

    medications_that_the_patient_is_on = []

    physical_examinations = []
    possible_diagnoses = []
    final_diagnosis = None
    treatment_name = None
    needs_to_go_to_doctor = None
    needs_advice = None

    common_knowledge = RelationStorage(
        name="Common Knowledge Relation Storage", is_private=False
    )

    # VALUES
    value_politeness = Value("politeness")
    values = [value_politeness]

    basic_competences = RelationStorage("Basic Competences")

    basic_competences.add_multi(
        [
            Competence(
                "Asking questions for information",
                RequestInfo(asked=AnyInformation(), tense=Tense.ANY),
            ),
            Competence(
                "Asking questions for yes or no answers",
                RequestConfirmation(
                    done_by=DSTPronoun.I,
                    asked=AnyInformation(),
                    tense=Tense.ANY,
                    recipient=DSTPronoun.YOU,
                    negation=Negation.ANY,
                    is_any=True,
                ),
            ),
            Competence(
                "Moving like walking",
                Move(
                    done_by=DSTPronoun.I,
                    moved=DSTPronoun.I,
                    from_place=AnyPlace(),
                    to_place=AnyPlace(),
                ),
            ),
            Competence(
                "Carrying a resource from a place to a place",
                Move(
                    done_by=DSTPronoun.I,
                    moved=AnyResource(),
                    from_place=AnyPlace(),
                    to_place=AnyPlace(),
                ),
            ),
            Competence(
                "Requesting actions",
                RequestAction(done_by=DSTPronoun.I, requested=AnyAction()),
            ),
            Competence("Greeting", Greet()),
            Competence("Backchannel", Backchannel()),
            Competence("Acknowledge", Acknowledge()),
            Competence("Selftalk", SelfTalk()),
            Competence("Learn", Learn(done_by=DSTPronoun.I, learned=AnyInformation())),
            Competence("Affirm", Affirm(AnyInformation())),
            Competence("Deny", Deny(AnyInformation())),
            Competence("Share", Share(information=AnyInformation())),
            Competence(
                "Feel",
                Feel(
                    done_by=DSTPronoun.I,
                    felt=AnyProperty(),
                    about=AnyRelation(),
                    r_tense=Tense.ANY,
                ),
            ),
            Competence("Thank", Thank()),
            Competence("Deduce", Deduce(done_by=DSTPronoun.I, deduced=AnyRelation())),
            Competence(
                "Check",
                Check(checked=AnyRelation(), r_tense=Tense.ANY, recipient=AnyAgent()),
            ),
            Competence(
                "Add expected action",
                SimpleAction(
                    name="doesnt matter",
                    done_by=DSTPronoun.I,
                    act_type=ActionObjType.ANY,
                    recipient=DSTPronoun.YOU,
                    target_resource=AnyResource(),
                    base_effects=[
                        AddExpectedEffect(effect=AnyEffect(), affected=AnyAgent())
                    ],
                ),
            ),
            Competence(
                "asd",
                RequestAction(
                    done_by=DSTPronoun.I,
                    recipient=DSTPronoun.YOU,
                    requested=Permit(
                        done_by=DSTPronoun.YOU,
                        permit_given_to=DSTPronoun.I,
                        permitted=AnyAction(),
                        r_tense=Tense.ANY,
                    ),
                ),
            ),
            Competence("Bye", Bye()),
        ]
    )

    # Agent 1's initialization
    agent_patient = Agent(
        name="Joe(patient)", actor=actor_patient, roles=[], auto=True
    )
    any_agent.dialogue_system = agent_patient.dialogue_system

    agent_patient.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)
    agent_patient.relation_storages[RSType.KNOWLEDGEBASE].add_multi(infos_symptom)

    agent_patient.relation_storages[RSType.COMPETENCES].add_from_rs(basic_competences)
    agent_patient.relation_storages[RSType.COMPETENCES].add(
        Competence(
            name="worry", action=Worry(about=AnyInformation()), negation=Negation.FALSE
        )
    )

    actor_doctor = Actor(
        name="doctor", knowledgebase=RelationStorage("doctor's Knowledgebase ")
    )
    agent2_permits = RelationStorage(actor_doctor.name + " Permits")

    # Agent 2's initialization
    agent_doctor = Agent(name="doctor", actor=actor_doctor, roles=[], auto=False)

    agent_doctor.relation_storages[RSType.COMPETENCES].add(
        Competence(name="doctor can examine eyes", action=Examine())
    )
    agent_doctor.relation_storages[RSType.COMPETENCES].add_from_rs(basic_competences)
    agent_doctor.relation_storages[RSType.COMPETENCES].add(
        Competence(
            name="calms down",
            action=CalmDown(about=AnyInformation()),
            negation=Negation.FALSE,
        )
    )
    agent_doctor.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)

    info_what_happened = Information(left=p_what_happened, rtype=RType.IS, rtense=Tense.PRESENT, right=AnyProperty())
    info_is_first_time = Information(left=p_is_first_time, rtype=RType.IS, rtense=Tense.PRESENT, right=AnyProperty())
    info_when_happened = Information(left=p_when_happened, rtype=RType.IS, rtense=Tense.PAST, right=AnyProperty())
    info_has_contact_lenses = Information(left=agent_patient, rtype=RType.HAS,
                                          rtense=Tense.PRESENT, right=p_has_contact_lenses)
    info_did_self_cure = Information(left=agent_patient, rtype=RType.HAS,
                                     rtense=Tense.PRESENT, right=p_did_self_cure)

    agent_patient.relation_storages[RSType.KNOWLEDGEBASE].add_multi([
        info_what_happened,
        info_when_happened,
        info_has_contact_lenses,
        info_is_first_time,
        info_did_self_cure
    ])

    utterances = [
        Utterance(text='Hi', actions=[
            Greet()
        ]),
        Utterance("Yes.", actions=[Affirm(affirmed=AnyInformation())]),
        Utterance("No.", actions=[Deny(denied=AnyInformation())]),
        Utterance(text='So, what brings you here today?', actions=[
            RequestInfo(asked=info_what_happened, tense=Tense.PRESENT)
        ]),
        Utterance(text=p_what_happened.name, actions=[
            Share(information=info_what_happened, tense=Tense.PRESENT)
        ]),
        Utterance(text='When did it happen?', actions=[
            RequestInfo(asked=info_when_happened)
        ]),
        Utterance(text=p_when_happened.name, actions=[
            Share(information=info_when_happened)
        ]),
        Utterance(text='Did you have this problem before?', actions=[
            RequestInfo(asked=info_is_first_time)
        ]),
        Utterance(text=p_is_first_time.name, actions=[
            Share(information=info_is_first_time)
        ]),
        Utterance(text='Do you wear contact lenses?', actions=[
            RequestInfo(asked=info_has_contact_lenses)
        ]),
        Utterance(text=p_has_contact_lenses.name, actions=[
            Share(information=info_has_contact_lenses)
        ]),
        Utterance(text='Did you try to cure it yourself?', actions=[
            RequestInfo(asked=info_did_self_cure)
        ]),
        Utterance(text=p_did_self_cure.name, actions=[
            Share(information=info_did_self_cure)
        ])
    ]

    # for info in infos_symptom:
    #     utterances.append(
    #         Utterance(text='Do you have ' + info.right.name + '?', actions=[
    #             RequestConfirmation(asked=info)
    #         ])
    #     )
    #     utterances.append(
    #         Utterance(text='Does your eye have ' + info.right.name + '?', actions=[
    #             RequestConfirmation(asked=info)
    #         ])
    #     )
    #     utterances.append(
    #         Utterance(text='Is your eye ' + info.right.name + '?', actions=[
    #             RequestConfirmation(asked=info)
    #         ])
    #     )

    for info in infos_symptom:
        utterances.append(
            Utterance(text='Do you have ' + info.right.name + '?', actions=[
                RequestConfirmation(asked=info)
            ])
        )
        utterances.append(
            Utterance(text='Does your eye have ' + info.right.name + '?', actions=[
                RequestConfirmation(asked=info)
            ])
        )
        utterances.append(
            Utterance(text='Is your eye ' + info.right.name + '?', actions=[
                RequestConfirmation(asked=info)
            ])
        )

    greeting_norm = Norm(
        name="People greet each other",
        start_conditions=[
            AgentDoesAction(
                agent=any_agent,
                action=Greet(),
                tense=Tense.PAST,
                negation=Negation.FALSE,
            )
        ],
        symbol_values={
            Placeholder("x"): "0.action.done_by",
            Placeholder("y"): "0.action.recipient",
        },
        steps=[
            ExpectationStep(
                action=Greet,
                action_attrs={
                    "done_by": Placeholder("y"),
                    "recipient": Placeholder("x"),
                },
                done_by=Placeholder("y"),
                recipient=Placeholder("x"),
            ),
        ],
        skipping_conditions=[
            AgentCanDo(
                agent=DSTPronoun.I,
                action=Greet(),
                tense=Tense.ANY,
                negation=Negation.TRUE,
            )
        ],
        completion_effects=[],
        violation_effects=[],
    )

    session_greeting = Session(
        name='Greeting',
        start_conditions=[

        ],
        expectations=[
            greeting_norm
        ],
        end_goals=[
            Goal(owner=any_agent,
                 name='greeting is finished',
                 conditions=[
                     ExpectationStatusIs(expectation=greeting_norm, expectation_status=ExpectationStatus.COMPLETED)
                 ],
                 known_by=[agent_patient, agent_doctor])
        ]
    )

    session_problem_presentation = Session(
        name='Problem Presentation',
        start_conditions=[
            ExpectationStatusIs(expectation=greeting_norm, expectation_status=ExpectationStatus.COMPLETED)
        ],
        expectations=[

        ],
        end_goals=[
            Goal(owner=agent_doctor,
                 name='doctor heard the problem',
                 conditions=[
                     AgentKnows(agent=agent_doctor, tense=Tense.PRESENT,
                                knows=info_what_happened)
                 ],
                 known_by=[agent_patient, agent_doctor]
                 )
        ]
    )

    session_history_taking = Session(
        name='History Taking',
        start_conditions=[
            AgentKnows(agent=agent_doctor, tense=Tense.PRESENT,
                       knows=info_what_happened)
        ],
        expectations=[],
        end_goals=[
            Goal(owner=any_agent,
                 name='doctors knows when happened',
                 conditions=[
                     AgentKnows(agent=agent_doctor, tense=Tense.PRESENT,
                                knows=info_when_happened)
                 ],
                 known_by=[agent_doctor]
                 ),
            Goal(owner=any_agent,
                 name='doctor knows if patient wears contact lenses',
                 conditions=[
                     AgentKnows(agent=agent_doctor, tense=Tense.PRESENT,
                                knows=info_has_contact_lenses)
                 ],
                 known_by=[agent_doctor]
                 ),
            Goal(owner=any_agent,
                 name='doctor knows if it is first time',
                 conditions=[
                     AgentKnows(agent=agent_doctor, tense=Tense.PRESENT,
                                knows=info_is_first_time)
                 ],
                 known_by=[agent_doctor]
                 ),
            # Goal(owner=any_agent,
            #      name='doctor heard the problem',
            #      conditions=[
            #          AgentKnows(agent=agent_doctor, tense=Tense.PRESENT,
            #                     knows=info_what_happened)
            #      ],
            #      known_by=[agent_patient, agent_doctor]
            #      )
        ]
    )

    sessions = [
        # session_global,
        session_greeting,
        session_problem_presentation,
        session_history_taking,
        # session_physical_examination,
        # session_diagnosis,
        # session_treatment,
        # session_closing,
    ]

    return Scenario(
        name="Eye Dialogue",
        agents=[agent_patient, agent_doctor],
        utterances=utterances,
        sessions=sessions,
        actions=[
            Greet,
            Thank,
            Move,
            Share,
            Permit,
            RequestAction,
            RequestInfo,
            RequestConfirmation,
            Affirm,
            Deny,
            Worry,
            CalmDown,
            Bye,
        ],
        effects=[
            ChangePlace,
            GainKnowledge,
            AddExpectedEffect,
            PromoteValue,
            DemoteValue,
        ],
        places=places,
        properties=properties,
        resources=resources,
        values=values,
    )
