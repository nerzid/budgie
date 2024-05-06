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
from socialds.any.any_information import AnyInformation
from socialds.conditions.has_permit import HasPermit
from socialds.conditions.session_status_is import SessionStatusIs
from socialds.expectation_step import ExpectationStep
from socialds.managers.dialogue_manager import DialogueManager
from socialds.managers.session_manager import SessionManager
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

SP_NAME = "Doctor's"


def sp_main():
    # Globals
    any_agent = AnyAgent()
    any_place = AnyPlace()
    places_office = Place("office")
    place_waiting_room = Place("waiting room")

    places_office.relation_storages[RSType.REQUIREMENTS].add(
        Requirement(
            required_for=ChangePlace(
                from_place=any_place, to_place=places_office, affected=DSTPronoun.I
            ),
            required=[
                HasPermit(
                    agent=DSTPronoun.I,
                    permit=ChangePlace(
                        from_place=any_place,
                        to_place=places_office,
                        affected=DSTPronoun.I,
                    ),
                )
            ],
        )
    )

    places = [places_office, place_waiting_room]

    actor1 = Actor(
        name="Joe", knowledgebase=RelationStorage("Actor Joe's Knowledgebase")
    )

    # RESOURCES
    p_patients_problem = Resource("patient's problem")
    p_patients_left_eye = Resource("left eye")
    p_patients_right_eye = Resource("right eye")
    p_patients_both_eyes = Resource("both eyes")
    p_veins_in_left_eye = Resource("veins in left eye")
    p_veins_in_right_eye = Resource("veins in right eye")
    p_eye = Resource("eye")
    p_inflammation = Resource("inflammation")
    p_medicine = Resource("medicine")
    p_bacterial_conjunctivitis = Resource("bacterial conjunctivitis")
    p_antibiotics = Resource("antibiotics")
    p_problem_description = Resource("problem description")
    resources = [
        p_patients_problem,
        p_patients_left_eye,
        p_patients_right_eye,
        p_patients_both_eyes,
        p_veins_in_left_eye,
        p_veins_in_right_eye,
        p_eye,
        p_inflammation,
        p_medicine,
        p_bacterial_conjunctivitis,
        p_antibiotics,
        p_problem_description,
    ]

    # PROPERTIES
    p_sick = Property("sick")
    p_teary = Property("teary")
    p_healthy = Property("healthy")
    p_blurry = Property("blurry")
    p_vision = Resource("vision")
    p_pain = Property("pain")
    p_painful = Property("painful")
    p_red = Property("red")
    p_worry = Property("worry")
    p_cold = Property("cold")
    p_swelling = Property("swelling")
    p_common = Property("common")
    p_symptom = Property("symptom")
    properties = [
        p_sick,
        p_teary,
        p_healthy,
        p_blurry,
        p_vision,
        p_pain,
        p_painful,
        p_red,
        p_worry,
        p_cold,
        p_swelling,
        p_common,
        p_symptom,
    ]

    common_knowledge = RelationStorage(
        name="Common Knowledge Relation Storage", is_private=False
    )

    common_knowledge.add_multi(
        [
            Information(
                left=p_patients_left_eye,
                rtype=RType.IS,
                rtense=Tense.PRESENT,
                right=p_eye,
            ),
            Information(
                left=p_patients_right_eye,
                rtype=RType.IS,
                rtense=Tense.PRESENT,
                right=p_eye,
            ),
            Information(
                left=Information(
                    left=p_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_teary
                ),
                rtype=RType.IS,
                rtense=Tense.PRESENT,
                right=p_symptom,
            ),
            Information(
                left=Information(
                    left=p_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_red
                ),
                rtype=RType.IS,
                rtense=Tense.PRESENT,
                right=p_symptom,
            ),
            Information(
                left=Information(
                    left=p_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_pain
                ),
                rtype=RType.IS,
                rtense=Tense.PRESENT,
                right=p_symptom,
            ),
            Information(
                left=Information(
                    left=p_eye,
                    rtype=RType.HAS,
                    rtense=Tense.PRESENT,
                    right=p_inflammation,
                ),
                rtype=RType.IS,
                rtense=Tense.PRESENT,
                right=p_symptom,
            ),
        ]
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
                "Add expected effect",
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
        ]
    )

    # Agent 1's initialization
    agent1 = Agent(name="Joe(patient)", actor=actor1, roles=[], auto=False)
    info_patient_is_sick = Information(
        left=actor1, rtype=RType.IS, rtense=Tense.PRESENT, right=p_sick
    )
    info_patient_has_left_eye = Information(
        left=actor1, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_patients_left_eye
    )
    info_patient_has_right_eye = Information(
        left=actor1, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_patients_right_eye
    )
    info_patients_left_eye_is_teary = Information(
        left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_teary
    )
    info_patients_left_eye_is_red = Information(
        left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_red
    )
    info_patients_left_eye_has_pain = Information(
        left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_pain
    )
    info_patients_eft_eye_has_vision = Information(
        left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_vision
    )
    info_patients_left_eye_has_veins = Information(
        left=p_patients_left_eye,
        rtype=RType.HAS,
        rtense=Tense.PRESENT,
        right=p_veins_in_left_eye,
    )
    info_patients_right_eye_has_veins = Information(
        left=p_patients_right_eye,
        rtype=RType.HAS,
        rtense=Tense.PRESENT,
        right=p_veins_in_right_eye,
    )
    info_patients_vision_is_blurry = Information(
        left=p_vision, rtype=RType.IS, rtense=Tense.PRESENT, right=p_blurry
    )
    info_patients_right_eye_is_healthy = Information(
        left=p_patients_right_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_healthy
    )
    info_problem_description_is_any = Information(
        left=p_problem_description,
        rtype=RType.IS,
        rtense=Tense.PRESENT,
        right=AnyProperty(),
    )

    info_patients_veins_in_left_eye_is_red = Information(
        left=p_veins_in_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_red
    )
    info_patients_veins_in_left_eye_is_red.relation_storages[RSType.REQUIREMENTS].add(
        Requirement(
            required_for=GainKnowledge(
                knowledge=info_patients_veins_in_left_eye_is_red, affected=DSTPronoun.I
            ),
            required=[
                AgentCanDo(DSTPronoun.I, Examine(), tense=Tense.ANY),
                AgentDoesAction(DSTPronoun.I, Examine(), tense=Tense.PAST),
            ],
        )
    )

    info_patients_left_eye_has_inflammation = Information(
        left=p_patients_left_eye,
        rtype=RType.HAS,
        rtense=Tense.PRESENT,
        right=p_inflammation,
    )
    info_patients_left_eye_has_inflammation.relation_storages[
        RSType.REQUIREMENTS
    ].add_multi(
        [
            Requirement(
                required_for=GainKnowledge(
                    knowledge=info_patients_left_eye_has_inflammation,
                    affected=DSTPronoun.I,
                ),
                required=[
                    AgentCanDo(DSTPronoun.I, Examine(), tense=Tense.ANY),
                    AgentDoesAction(DSTPronoun.I, Examine(), tense=Tense.PAST),
                    AgentKnows(
                        DSTPronoun.I,
                        knows=info_patients_veins_in_left_eye_is_red,
                        tense=Tense.PRESENT,
                    ),
                ],
            ),
        ]
    )

    info_patients_left_eye_has_bacterial_conjunctivitis = Information(
        left=p_patients_left_eye,
        rtype=RType.HAS,
        rtense=Tense.PRESENT,
        right=p_bacterial_conjunctivitis,
    )
    info_patients_left_eye_has_bacterial_conjunctivitis.relation_storages[
        RSType.REQUIREMENTS
    ].add_multi(
        [
            Requirement(
                required_for=Deduce(
                    done_by=DSTPronoun.I,
                    deduced=info_patients_left_eye_has_bacterial_conjunctivitis,
                ),
                required=[
                    AgentKnows(
                        DSTPronoun.I,
                        knows=info_patients_left_eye_has_inflammation,
                        tense=Tense.PRESENT,
                    ),
                    AgentKnows(
                        DSTPronoun.I,
                        knows=info_patients_veins_in_left_eye_is_red,
                        tense=Tense.PRESENT,
                    ),
                ],
            )
        ]
    )

    info_patients_problem_is_bacterial_conjunctivitis = Information(
        left=p_patients_problem,
        rtype=RType.IS,
        rtense=Tense.PRESENT,
        right=p_bacterial_conjunctivitis,
    )

    info_patients_left_eye_has_swelling = Information(
        left=p_patients_left_eye,
        rtype=RType.HAS,
        rtense=Tense.PRESENT,
        right=p_swelling,
    )

    p_veins_in_left_eye.relation_storages[RSType.PROPERTIES].add(
        info_patients_veins_in_left_eye_is_red
    )

    info_patients_problem_is_bacterial_conjunctivitis.relation_storages[
        RSType.REQUIREMENTS
    ].add_multi(
        [
            Requirement(
                required_for=Deduce(
                    done_by=DSTPronoun.I,
                    deduced=info_patients_problem_is_bacterial_conjunctivitis,
                ),
                required=[
                    AgentKnows(
                        DSTPronoun.I,
                        knows=info_patients_left_eye_has_inflammation,
                        tense=Tense.PRESENT,
                    ),
                    AgentKnows(
                        DSTPronoun.I,
                        knows=info_patients_veins_in_left_eye_is_red,
                        tense=Tense.PRESENT,
                    ),
                ],
            ),
            Requirement(
                required_for=GainKnowledge(
                    knowledge=info_patients_left_eye_has_swelling, affected=DSTPronoun.I
                ),
                required=[
                    AgentDoesAction(
                        agent=DSTPronoun.I, action=Examine(), tense=Tense.PAST
                    )
                ],
            ),
        ]
    )

    info_patient_had_cold = Information(
        left=DSTPronoun.YOU, rtype=RType.HAS, rtense=Tense.PAST, right=p_cold
    )

    agent1.relation_storages[RSType.KNOWLEDGEBASE].add_multi(
        [
            info_patient_is_sick,
            info_patient_has_left_eye,
            info_patient_has_right_eye,
            info_patients_left_eye_is_teary,
            info_patients_left_eye_is_red,
            info_patients_left_eye_has_pain,
            info_patients_eft_eye_has_vision,
            info_patients_left_eye_has_veins,
            info_patients_right_eye_has_veins,
            info_patients_vision_is_blurry,
            info_patients_right_eye_is_healthy,
            info_patients_left_eye_has_swelling,
            info_problem_description_is_any,
        ]
    )
    agent1.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)
    agent1.relation_storages[RSType.PLACES].add_multi(
        [
            # Relation(left=agent1, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=any_place),
            Relation(
                left=agent1,
                rtype=RType.IS_AT,
                rtense=Tense.PRESENT,
                right=place_waiting_room,
            )
        ]
    )
    agent1.relation_storages[RSType.COMPETENCES].add_from_rs(basic_competences)

    actor2 = Actor(
        name="Jane", knowledgebase=RelationStorage("Actor Jane's Knowledgebase ")
    )
    agent2_permits = RelationStorage(actor2.name + " Permits")

    # Agent 2's initialization
    agent2 = Agent(name="Jane(doctor)", actor=actor2, roles=[], auto=True)

    agent2.relation_storages[RSType.COMPETENCES].add(
        Competence(
            name="doctor can let patients in his office",
            action=Permit(
                done_by=DSTPronoun.I,
                permitted=ChangePlace(
                    from_place=any_place,
                    to_place=places_office,
                    affected=DSTPronoun.YOU,
                ),
                permit_given_to=DSTPronoun.YOU,
                r_tense=Tense.ANY,
            ),
        )
    )
    agent2.relation_storages[RSType.COMPETENCES].add(
        Competence(name="doctor can examine eyes", action=Examine())
    )
    agent2.relation_storages[RSType.COMPETENCES].add_from_rs(basic_competences)
    agent2.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)
    agent2.relation_storages[RSType.PERMITS].add_multi(
        [
            Relation(
                left=agent2,
                rtype=RType.IS_PERMITTED_TO,
                rtense=Tense.ANY,
                right=ChangePlace(
                    from_place=any_place,
                    to_place=places_office,
                    affected=DSTPronoun.YOU,
                ),
            ),
            Relation(
                left=agent2,
                rtype=RType.IS_PERMITTED_TO,
                rtense=Tense.ANY,
                right=Permit(
                    done_by=DSTPronoun.I,
                    permit_given_to=DSTPronoun.YOU,
                    permitted=ChangePlace(
                        from_place=any_place,
                        to_place=places_office,
                        affected=DSTPronoun.YOU,
                    ),
                    r_tense=Tense.PRESENT,
                ),
            ),
        ]
    )

    agent2.relation_storages[RSType.PLACES].add_multi(
        [
            # Relation(left=agent2, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=any_place),
            Relation(
                left=agent2,
                rtype=RType.IS_AT,
                rtense=Tense.PRESENT,
                right=places_office,
            )
        ]
    )

    # Actions
    action_examine = Information(
        left=DSTPronoun.I, rtype=RType.ACTION, rtense=Tense.FUTURE, right=Examine()
    )

    # Utterances
    utterances = [
        Utterance("Does nothing", []),
        Utterance("Hi!", [Greet()]),
        Utterance(
            "Hi, come in.",
            [
                Greet(),
                Then(),
                Permit(
                    done_by=DSTPronoun.I,
                    permitted=Move(
                        done_by=DSTPronoun.YOU,
                        moved=DSTPronoun.YOU,
                        from_place=any_place,
                        to_place=places_office,
                    ),
                    r_tense=Tense.PRESENT,
                    permit_given_to=DSTPronoun.YOU,
                ),
            ],
        ),
        Utterance(
            "Can I come in?",
            [
                RequestAction(
                    done_by=DSTPronoun.I,
                    requested=Permit(
                        done_by=DSTPronoun.YOU,
                        permitted=Move(
                            done_by=DSTPronoun.I,
                            moved=DSTPronoun.I,
                            from_place=any_place,
                            to_place=places_office,
                        ),
                        r_tense=Tense.PRESENT,
                        permit_given_to=DSTPronoun.I,
                    ),
                )
            ],
        ),
        Utterance(
            "Yes, please.",
            [
                Permit(
                    done_by=DSTPronoun.I,
                    permitted=Move(
                        done_by=DSTPronoun.YOU,
                        moved=DSTPronoun.YOU,
                        from_place=any_place,
                        to_place=places_office,
                    ),
                    r_tense=Tense.PRESENT,
                    permit_given_to=DSTPronoun.YOU,
                )
            ],
        ),
        Utterance(
            "Thank you. (Moves to doctor's office)",
            [
                Thank(),
                And(),
                Move(
                    done_by=DSTPronoun.I,
                    moved=DSTPronoun.I,
                    from_place=place_waiting_room,
                    to_place=places_office,
                ),
            ],
        ),
        Utterance(
            "So, what brings you here today?",
            [RequestInfo(asked=info_problem_description_is_any, tense=Tense.PRESENT)],
        ),
        Utterance(
            "My left eye has been red since this morning.",
            [Share(information=info_problem_description_is_any)],
        ),
        Utterance(
            "Is your vision blurry?",
            [
                RequestConfirmation(
                    done_by=DSTPronoun.I,
                    asked=info_patients_vision_is_blurry,
                    tense=Tense.PRESENT,
                    recipient=DSTPronoun.YOU,
                )
            ],
        ),
        Utterance(
            "Yes, I have a blurry vision",
            [Affirm(affirmed=info_patients_vision_is_blurry)],
        ),
        Utterance("Hm hmm...", [Backchannel()]),
        Utterance(
            "and it hurts a lot.",
            [
                Share(
                    information=Information(
                        left=p_patients_left_eye,
                        rtype=RType.HAS,
                        rtense=Tense.PRESENT,
                        right=p_pain,
                    )
                )
            ],
        ),
        Utterance(
            "Did you take any medicine to ease your pain?",
            [
                Check(
                    r_tense=Tense.PRESENT,
                    checked=Relation(
                        left=DSTPronoun.YOU,
                        rtype=RType.ACTION,
                        rtense=Tense.PAST,
                        right=Take(
                            taken=p_medicine,
                            done_by=DSTPronoun.YOU,
                            r_tense=Tense.PRESENT,
                        ),
                    ),
                    recipient=DSTPronoun.YOU,
                )
            ],
        ),
        Utterance(
            "No, I was worried that would make it worse.",
            [
                Feel(
                    done_by=DSTPronoun.I,
                    felt=p_worry,
                    about=Relation(
                        left=DSTPronoun.I,
                        rtype=RType.ACTION,
                        rtense=Tense.PRESENT,
                        right=Take(
                            r_tense=Tense.PRESENT,
                            taken=p_medicine,
                            done_by=DSTPronoun.I,
                        ),
                    ),
                    r_tense=Tense.PAST,
                )
            ],
        ),
        Utterance("I see.", [Acknowledge()]),
        Utterance(
            "Do you have any tears?",
            [
                # Check(checked=Relation(left=p_patients_left_eye, rtype=RType.IS,
                #                        rtense=Tense.PRESENT, negation=False,
                #                        right=p_teary),
                #       r_tense=Tense.PRESENT,
                #       negation=False,
                #       recipient=DSTPronoun.YOU),
                RequestConfirmation(
                    done_by=DSTPronoun.I,
                    asked=info_patients_left_eye_is_teary,
                    tense=Tense.PRESENT,
                    recipient=DSTPronoun.YOU,
                )
            ],
        ),
        Utterance(
            "Yes, my left eye is teary.",
            [
                Affirm(affirmed=info_patients_left_eye_is_teary),
                # Then(),
                # Share(information=info_patients_left_eye_is_teary)
            ],
        ),
        Utterance(
            "Okay, I need to examine your eye now if that's okay for you.",
            [
                RequestConfirmation(
                    done_by=DSTPronoun.I,
                    asked=action_examine,
                    tense=Tense.PRESENT,
                    recipient=DSTPronoun.YOU,
                ),
                # RequestAction(done_by=DSTPronoun.I, requested=Examine()),
                And(),
                Notify(
                    notified_about=action_examine,
                    recipient=DSTPronoun.YOU,
                    done_by=DSTPronoun.I,
                ),
            ],
        ),
        Utterance("Okay.", [Affirm(affirmed=action_examine)]),
        Utterance(
            "Will it hurt?",
            [
                Check(
                    r_tense=Tense.PRESENT,
                    checked=Information(
                        left=Information(
                            left=DSTPronoun.YOU,
                            rtype=RType.ACTION,
                            rtense=Tense.PRESENT,
                            right=Examine(),
                        ),
                        rtype=RType.IS,
                        rtense=Tense.PRESENT,
                        right=p_painful,
                    ),
                    recipient=DSTPronoun.YOU,
                )
            ],
        ),
        Utterance(
            "No, you will just feel mild pressure in your eye, but it shouldn't hurt.",
            [
                # Deny(),
                And(),
                Share(
                    information=Information(
                        left=Information(
                            left=DSTPronoun.I,
                            rtype=RType.ACTION,
                            rtense=Tense.PRESENT,
                            right=Examine(),
                        ),
                        rtype=RType.IS,
                        rtense=Tense.PRESENT,
                        right=p_painful,
                        negation=Negation.TRUE,
                    )
                ),
            ],
        ),
        Utterance(
            "You can tell me if it hurts or you just feel uncomfortable.",
            [
                When(
                    action=Notify(
                        recipient=DSTPronoun.I,
                        notified_about=Feel(
                            felt=p_pain,
                            done_by=DSTPronoun.YOU,
                            r_tense=Tense.PRESENT,
                            about=Relation(
                                left=DSTPronoun.I,
                                rtype=RType.ACTION,
                                rtense=Tense.PRESENT,
                                right=Examine(),
                            ),
                        ),
                        done_by=DSTPronoun.I,
                    ),
                    conditions=[
                        AgentDoesAction(
                            agent=DSTPronoun.YOU,
                            tense=Tense.PRESENT,
                            action=Feel(
                                done_by=DSTPronoun.YOU,
                                felt=p_pain,
                                r_tense=Tense.PRESENT,
                                about=Relation(
                                    left=DSTPronoun.I,
                                    rtype=RType.ACTION,
                                    rtense=Tense.PRESENT,
                                    right=Examine(),
                                ),
                            ),
                        )
                    ],
                )
            ],
        ),
        Utterance("Okay doctor, thank you.", [Acknowledge(), Then(), Thank()]),
        Utterance(
            "Can you open your eyes now?",
            [
                RequestAction(
                    requested=Open(
                        target_resource=p_patients_both_eyes, done_by=DSTPronoun.YOU
                    ),
                    done_by=DSTPronoun.I,
                )
            ],
        ),
        Utterance("Perfect.", [Acknowledge()]),
        Utterance("Let me see.", [SelfTalk()]),
        Utterance(
            "I see that the veins in your left eye are red.",
            [
                Learn(
                    learned=info_patients_veins_in_left_eye_is_red, done_by=DSTPronoun.I
                ),
                And(),
                Share(information=info_patients_veins_in_left_eye_is_red),
            ],
        ),
        Utterance(
            "And there is inflammation.",
            [
                Learn(
                    learned=info_patients_left_eye_has_inflammation,
                    done_by=DSTPronoun.I,
                ),
                And(),
                Share(information=info_patients_left_eye_has_inflammation),
            ],
        ),
        Utterance(
            "Okay.",
            [
                SelfTalk(),
                And(),
                Deduce(
                    done_by=DSTPronoun.I,
                    deduced=info_patients_left_eye_has_bacterial_conjunctivitis,
                ),
                And(),
                Deduce(
                    done_by=DSTPronoun.I,
                    deduced=info_patients_problem_is_bacterial_conjunctivitis,
                ),
            ],
        ),
        Utterance(
            "So, what is the problem with my eye?",
            [
                RequestInfo(
                    asked=Information(
                        left=p_patients_problem,
                        rtype=RType.IS,
                        rtense=Tense.PRESENT,
                        right=AnyProperty(),
                    ),
                    tense=Tense.PRESENT,
                ),
                # Or(),
                # RequestInfo(asked=Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                #                            right=AnyProperty()),
                #             r_tense=Tense.PRESENT)
            ],
        ),
        Utterance(
            "Your left eye has bacterial conjunctivitis.",
            [
                Share(
                    information=Information(
                        left=p_patients_left_eye,
                        rtype=RType.HAS,
                        rtense=Tense.PRESENT,
                        right=p_bacterial_conjunctivitis,
                    )
                )
            ],
        ),
        Utterance(
            "Did you have a cold recently?",
            [
                Check(
                    r_tense=Tense.PRESENT,
                    checked=info_patient_had_cold,
                    recipient=DSTPronoun.YOU,
                )
            ],
        ),
        Utterance(
            "Yes, is that why?",
            [
                Affirm(affirmed=info_patient_had_cold),
                And(),
                Share(
                    information=Information(
                        left=DSTPronoun.I,
                        rtype=RType.HAS,
                        rtense=Tense.PAST,
                        right=p_cold,
                    )
                ),
            ],
        ),
        Utterance(
            "Yeah, it is pretty common to get bacterial conjunctivitis after having a cold.",
            [
                Share(
                    information=Information(
                        left=Information(
                            left=p_eye,
                            rtype=RType.HAS,
                            rtense=Tense.PRESENT,
                            right=p_bacterial_conjunctivitis,
                        ),
                        rtype=RType.IS,
                        rtense=Tense.PRESENT,
                        right=p_common,
                        times=[After(after=Have(done_by=any_agent, target=p_cold))],
                    )
                )
            ],
        ),
        Utterance("Oh...", [Acknowledge()]),
        Utterance(
            "I will prescribe you some antibiotics, take them twice a day, one in the morning and one before you sleep.",
            [
                Prescribe(
                    done_by=DSTPronoun.I,
                    prescribed=[p_antibiotics],
                    recipient=DSTPronoun.YOU,
                ),
                And(),
                RequestAction(
                    done_by=DSTPronoun.I,
                    requested=Take(
                        done_by=DSTPronoun.YOU,
                        taken=p_antibiotics,
                        r_tense=Tense.PRESENT,
                        times=[
                            InMorning(num_of_times=NumOfTimes(1)),
                            Before(
                                Sleep(done_by=DSTPronoun.YOU),
                                num_of_times=NumOfTimes(1),
                            ),
                        ],
                    ),
                ),
            ],
        ),
        Utterance("Thank you, doctor.", [Thank()]),
        Utterance(
            "If it doesn't heal in a week, you can come again.",
            [
                When(
                    conditions=[
                        ActionOnResourceHappens(
                            resource=p_patients_left_eye,
                            tense=Tense.PRESENT,
                            action=Heal(
                                healed=p_patients_left_eye,
                                negation=Negation.TRUE,
                                times=[InWeek(num=1)],
                            ),
                        )
                    ],
                    action=Move(
                        done_by=DSTPronoun.YOU,
                        moved=DSTPronoun.YOU,
                        from_place=any_place,
                        to_place=places_office,
                    ),
                )
            ],
        ),
    ]

    basic_utterances = [
        Utterance("Hi", actions=[Greet()]),
        Utterance("Thank you.", actions=[Thank()]),
        Utterance("Yes.", actions=[Affirm(affirmed=AnyInformation())]),
        Utterance("No.", actions=[Deny(denied=AnyInformation())]),
    ]

    utterances.extend(basic_utterances)

    greeting_norm = Norm(
        name="People greet each other",
        steps=[
            ExpectationStep(
                action=Greet(),
                done_by=AgentPlaceholder(symbol=PlaceholderSymbol.X),
                recipient=AgentPlaceholder(symbol=PlaceholderSymbol.Y),
            ),
            ExpectationStep(
                action=Greet(),
                done_by=AgentPlaceholder(symbol=PlaceholderSymbol.Y),
                recipient=AgentPlaceholder(symbol=PlaceholderSymbol.X),
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
        completion_effects=[
            PromoteValue(affected=DSTPronoun.EVERYONE, value=value_politeness)
        ],
        violation_effects=[DemoteValue(affected=DSTPronoun.I, value=value_politeness)],
    )

    goodbye_norm = Norm(
        name="People said goodbye to each other",
        steps=[
            ExpectationStep(
                action=Bye(),
                done_by=AgentPlaceholder(symbol=PlaceholderSymbol.X),
                recipient=AgentPlaceholder(symbol=PlaceholderSymbol.Y),),
            ExpectationStep(
                action=Bye(),
                done_by=AgentPlaceholder(symbol=PlaceholderSymbol.Y),
                recipient=AgentPlaceholder(symbol=PlaceholderSymbol.X)
                ),
        ],
        skipping_conditions=[
            AgentCanDo(
                agent=DSTPronoun.I,
                action=Bye(),
                tense=Tense.ANY,
                negation=Negation.TRUE,
            )
        ],
        completion_effects=[],
        violation_effects=[],
    )

    # vars.expectations.append(greeting_norm)

    session_greeting = Session(
        name="Greeting",
        start_conditions=[
            AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=place_waiting_room),
            AgentAtPlace(agent=agent2, tense=Tense.PRESENT, place=places_office),
        ],
        expectations=[greeting_norm],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Patient is ready",
                desc="Patient and doctor greeted each other and patient is ready to talk",
                conditions=[
                    ExpectationStatusIs(
                        expectation=greeting_norm,
                        expectation_status=ExpectationStatus.COMPLETED,
                    ),
                    AgentAtPlace(
                        agent=agent1, tense=Tense.PRESENT, place=places_office
                    ),
                ],
            )
        ],
    )
    session_problem_presentation = Session(
        name="Problem Presentation",
        start_conditions=[
            ExpectationStatusIs(
                expectation=greeting_norm,
                expectation_status=ExpectationStatus.COMPLETED,
            ),
            AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=places_office),
        ],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Patient explained the problem",
                conditions=[
                    AgentKnows(
                        agent=agent2,
                        tense=Tense.PRESENT,
                        knows=info_problem_description_is_any,
                    )
                ],
            )
        ],
    )
    session_history_taking = Session(
        name="History Taking",
        start_conditions=[
            AgentKnows(
                agent=agent2, tense=Tense.PRESENT, knows=info_problem_description_is_any
            )
        ],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Doctor asked all the necessary questions before physical examination",
                conditions=[
                    AgentKnows(
                        agent=agent2,
                        tense=Tense.PRESENT,
                        knows=Information(
                            left=p_patients_left_eye,
                            rtype=RType.IS,
                            rtense=Tense.PRESENT,
                            right=p_teary,
                            negation=Negation.ANY,
                        ),
                    ),
                    AgentKnows(
                        agent=agent2,
                        tense=Tense.PRESENT,
                        knows=Information(
                            left=p_vision,
                            rtype=RType.IS,
                            rtense=Tense.PRESENT,
                            right=p_blurry,
                            negation=Negation.ANY,
                        ),
                    ),
                ],
            )
        ],
    )

    session_physical_examination = Session(
        name="Physical Examination",
        start_conditions=[
            SessionStatusIs(
                session=session_history_taking, session_status=SessionStatus.COMPLETED
            )
        ],
        expectations=[],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Doctor learnt all of the necessary symptoms from the examination",
                conditions=[
                    AgentKnows(
                        agent=agent2,
                        tense=Tense.PRESENT,
                        knows=info_patients_left_eye_has_inflammation,
                    ),
                    AgentKnows(
                        agent=agent2,
                        tense=Tense.PRESENT,
                        knows=info_patients_left_eye_has_swelling,
                    ),
                ],
            )
        ],
    )

    session_diagnosis = Session(
        name="Diagnosis",
        start_conditions=[
            SessionStatusIs(
                session=session_physical_examination,
                session_status=SessionStatus.COMPLETED,
            )
        ],
        expectations=[],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Patient knows the name of the problem",
                conditions=[
                    AgentKnows(
                        agent=agent1,
                        knows=info_patients_problem_is_bacterial_conjunctivitis,
                        tense=Tense.PRESENT,
                    )
                ],
            )
        ],
    )

    session_treatment = Session(
        name="Treatment and Recommendations",
        start_conditions=[
            SessionStatusIs(
                session=session_diagnosis, session_status=SessionStatus.COMPLETED
            )
        ],
        expectations=[],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Patient knows the treatment",
                conditions=[
                    AgentKnows(
                        agent=agent1,
                        knows=info_patients_problem_is_bacterial_conjunctivitis,
                        tense=Tense.PRESENT,
                    )
                ],
            )
        ],
    )

    session_closing = Session(
        name="Closing",
        start_conditions=[
            SessionStatusIs(
                session=session_treatment, session_status=SessionStatus.COMPLETED
            )
        ],
        expectations=[goodbye_norm],
        end_goals=[
            Goal(
                owner=any_agent,
                name="People said good bye to each other",
                conditions=[
                    ExpectationStatusIs(
                        expectation=goodbye_norm,
                        expectation_status=ExpectationStatus.COMPLETED,
                    )
                ],
            )
        ],
    )

    session_global = Session(
        name="Global",
        start_conditions=[],
        expectations=[],
        end_goals=[
            Goal(
                owner=any_agent,
                name="Social practice finished",
                conditions=[
                    SessionStatusIs(
                        session=session_history_taking,
                        session_status=SessionStatus.COMPLETED,
                    )
                ],
            )
        ],
    )
    sessions = [
        session_global,
        session_greeting,
        session_problem_presentation,
        session_history_taking,
        session_physical_examination,
        session_diagnosis,
        session_treatment,
        session_closing,
    ]

    return Scenario(
        name="Doctors visit",
        agents=[agent1, agent2],
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
