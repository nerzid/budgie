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
    p_what_happened = None
    symptoms = []
    r_left_eye = None
    r_right_eye = None
    r_both_eyes = None
    p_when_did_it_happen = None
    p_age_group = None

    p_has_the_patient_had_this_problem_before = None
    r_contact_lenses = None
    p_has_the_patient_tried_to_cure_himself = None
    p_did_the_patient_take_any_drugs_for_his_problem = None

    p_does_the_patient_have_any_allergies = None
    p_does_the_patient_have_any_rheumatic_diseases = None
    p_does_the_patients_relatives_have_the_same_problem = None

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
        name="Joe(patient)", actor=actor_patient, roles=[], auto=False
    )

    agent_patient.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)

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
    agent_doctor = Agent(name="doctor", actor=actor_doctor, roles=[], auto=True)

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

    utterances = []


    sessions = [
        # session_global,
        # session_greeting,
        # session_problem_presentation,
        # session_history_taking,
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
