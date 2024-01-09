from socialds.action.effects.functional.change_place import ChangePlace
from socialds.conditions.has_permit import HasPermit
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
from socialds.action.actions.verbal.ask import Ask
from socialds.action.actions.verbal.backchannel import Backchannel
from socialds.action.actions.verbal.check import Check
from socialds.action.actions.verbal.greet import Greet
from socialds.action.actions.verbal.have import Have
from socialds.action.actions.verbal.learn import Learn
from socialds.action.actions.verbal.deny import Deny
from socialds.action.actions.verbal.notify import Notify
from socialds.action.actions.verbal.request import Request
from socialds.action.actions.verbal.selftalk import SelfTalk
from socialds.action.actions.verbal.share import Share
from socialds.action.actions.verbal.thank import Thank
from socialds.action.actions.verbal.affirm import Affirm
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
from socialds.conditions.action_on_property_happens import ActionOnPropertyHappens
from socialds.conditions.agent_at_place import AgentAtPlace
from socialds.conditions.agent_can_do import AgentCanDo
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.conditions.agent_knows import AgentKnows
from socialds.conditions.expectation_status_is import ExpectationStatusIs
from socialds.conditions.norm_status_is import NormStatusIs
from socialds.dialogue_system import DialogueSystem
from socialds.enums import Tense
from socialds.expectation import ExpectationStatus
from socialds.goal import Goal
from socialds.managers.managers import session_manager
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RelationStorage, RSType, merge_relation_storages
from socialds.session import Session
from socialds.socialpractice.activity.competence import Competence
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.expectation.norm import Norm
from socialds.states.property import Property
from socialds.states.relation import Relation, RType
from socialds.states.value import Value
from socialds.utterance import Utterance
import socialds.other.variables as vars


def sp_main():
    # Global properties
    any_agent = AnyAgent()
    any_place = AnyPlace()
    places_office = Place('office')
    place_waiting_room = Place('waiting room')

    places_office.relation_storages[RSType.REQUIREMENTS].add(
        Requirement(
            required_for=ChangePlace(from_place=any_place,
                                     to_place=places_office,
                                     affected=DSTPronoun.I),
            required=[HasPermit(agent=DSTPronoun.I,
                                permit=ChangePlace(from_place=any_place,
                                                   to_place=places_office,
                                                   affected=DSTPronoun.I))])
    )

    actor1 = Actor(name="Joe", knowledgebase=RelationStorage('Actor Joe\'s Knowledgebase'))

    # Agent 1's properties
    p_patients_problem = Property("patient's problem")
    p_patients_left_eye = Property("left eye")
    p_patients_right_eye = Property("right eye")
    p_patients_both_eyes = Property('both eyes')
    p_veins_in_left_eye = Property('veins in left eye')
    p_veins_in_right_eye = Property('veins in right eye')
    p_eye = Property('eye')

    p_sick = Property('sick')
    p_teary = Property('teary')
    p_healthy = Property('healthy')
    p_blurry = Property('blurry')
    p_vision = Property('vision')
    p_pain = Property('pain')
    p_painful = Property('painful')
    p_red = Property('red')
    p_worry = Property('worry')
    p_inflammation = Property('inflammation')
    p_medicine = Property('medicine')
    p_bacterial_conjunctivitis = Property('bacterial conjunctivitis')
    p_cold = Property('cold')
    p_antibiotics = Property('antibiotics')
    p_common = Property('common')
    p_symptom = Property('symptom')
    p_problem_description = Property('problem description')

    common_knowledge = RelationStorage(name='Common Knowledge Relation Storage', is_private=False)

    common_knowledge.add_multi([
        Relation(left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_eye),
        Relation(left=p_patients_right_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_eye),
        Relation(left=Relation(left=p_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_teary), rtype=RType.IS,
                 rtense=Tense.PRESENT, right=p_symptom),
        Relation(left=Relation(left=p_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_red), rtype=RType.IS,
                 rtense=Tense.PRESENT, right=p_symptom),
        Relation(left=Relation(left=p_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_pain), rtype=RType.IS,
                 rtense=Tense.PRESENT, right=p_symptom),
        Relation(left=Relation(left=p_eye, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_inflammation), rtype=RType.IS,
                 rtense=Tense.PRESENT, right=p_symptom),
    ])

    # VALUES
    value_politeness = Value('politeness')

    basic_competences = RelationStorage('Basic Competences')

    basic_competences.add_multi([
        Competence('Asking questions', Ask(asked=AnyRelation(), r_tense=Tense.ANY)),
        Competence('Moving like walking',
                   Move(done_by=DSTPronoun.I, moved=DSTPronoun.I, from_place=AnyPlace(), to_place=AnyPlace())),
        Competence('Carrying a resource from a place to a place',
                   Move(done_by=DSTPronoun.I, moved=AnyResource(), from_place=AnyPlace(), to_place=AnyPlace())),
        Competence('Requesting things', Request(done_by=DSTPronoun.I, requested=AnyAction())),
        Competence('Greeting', Greet()),
        Competence('Backchannel', Backchannel()),
        Competence('Acknowledge', Acknowledge()),
        Competence('Selftalk', SelfTalk()),
        Competence('Learn', Learn(done_by=DSTPronoun.I, learned=AnyRelation())),
        Competence('Affirm', Affirm()),
        Competence('Deny', Deny()),
        Competence('Share', Share(relation=AnyRelation())),
        Competence('Feel', Feel(done_by=DSTPronoun.I, felt=AnyProperty(), about=AnyRelation(), r_tense=Tense.ANY)),
        Competence('Thank', Thank()),
        Competence('Deduce', Deduce(done_by=DSTPronoun.I, deduced=AnyRelation())),
        Competence('Check', Check(checked=AnyRelation(), r_tense=Tense.ANY, recipient=AnyAgent())),
        Competence('Add expected effect', SimpleAction(name='doesnt matter', done_by=DSTPronoun.I,
                                                       act_type=ActionObjType.ANY, recipient=DSTPronoun.YOU,
                                                       target_resource=AnyResource(),
                                                       base_effects=[
                                                           AddExpectedEffect(effect=AnyEffect(), negation=False,
                                                                             affected=AnyAgent())]))
    ])

    # Agent 1's initialization
    agent1 = Agent(name='Joe(patient)', actor=actor1, roles=[], auto=False)
    agent1.relation_storages[RSType.KNOWLEDGEBASE].add_multi([
        Relation(left=actor1, rtype=RType.IS, rtense=Tense.PRESENT, right=p_sick),
        Relation(left=actor1, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_patients_left_eye),
        Relation(left=actor1, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_patients_right_eye),
        Relation(left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_teary),
        Relation(left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_red),
        Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_pain),
        Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT, right=p_vision),
        Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                 right=p_veins_in_left_eye),
        Relation(left=p_patients_right_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                 right=p_veins_in_right_eye),
        Relation(left=p_vision, rtype=RType.IS, rtense=Tense.PRESENT, right=p_blurry),
        Relation(left=p_patients_right_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_healthy),
        Relation(left=p_problem_description, rtype=RType.IS, rtense=Tense.PRESENT, right=AnyProperty())
    ])
    agent1.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)
    agent1.relation_storages[RSType.PLACES].add_multi([
        # Relation(left=agent1, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=any_place),
        Relation(left=agent1, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=place_waiting_room)
    ])
    agent1.relation_storages[RSType.COMPETENCES].add_from_rs(basic_competences)

    actor2 = Actor(name="Jane", knowledgebase=RelationStorage('Actor Jane\'s Knowledgebase '))
    agent2_permits = RelationStorage(actor2.name + ' Permits')

    # Agent 2's initialization
    agent2 = Agent(name='Jane(doctor)',
                   actor=actor2,
                   roles=[],
                   auto=True
                   )

    # agent2_competences.add(Competence(name='doctor can let patients in his office',
    #                                   action=Permit(done_by=DSTPronoun.I,
    #                                                 permitted=Move(done_by=DSTPronoun.I,
    #                                                                moved=DSTPronoun.I,
    #                                                                from_place=any_place,
    #                                                                to_place=places_office),
    #                                                 permit_given_to=DSTPronoun.YOU,
    #                                                 r_tense=Tense.ANY,
    #                                                 negation=False)))
    agent2.relation_storages[RSType.COMPETENCES].add(Competence(name='doctor can let patients in his office',
                                                                action=Permit(done_by=DSTPronoun.I,
                                                                              permitted=ChangePlace(
                                                                                  from_place=any_place,
                                                                                  to_place=places_office,
                                                                                  affected=DSTPronoun.YOU),
                                                                              permit_given_to=DSTPronoun.YOU,
                                                                              r_tense=Tense.ANY,
                                                                              negation=False)))
    agent2.relation_storages[RSType.COMPETENCES].add_from_rs(basic_competences)
    agent2.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(common_knowledge)
    agent2.relation_storages[RSType.PERMITS].add(
        Relation(left=agent2, rtype=RType.IS_PERMITTED_TO, rtense=Tense.ANY, negation=False,
                 right=ChangePlace(from_place=any_place,
                                   to_place=places_office,
                                   affected=DSTPronoun.I)))

    agent2.relation_storages[RSType.PLACES].add_multi([
        # Relation(left=agent2, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=any_place),
        Relation(left=agent2, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=places_office)
    ])

    # Utterances
    utterances = [
        Utterance("Hi!", [
            Greet()
        ]),
        Utterance("Hi, come in", [
            Greet(),
            Then(),
            Permit(done_by=DSTPronoun.I,
                   permitted=Move(done_by=DSTPronoun.YOU,
                                  moved=DSTPronoun.YOU,
                                  from_place=any_place,
                                  to_place=places_office),
                   r_tense=Tense.PRESENT, negation=False, permit_given_to=DSTPronoun.YOU)
        ]),
        Utterance("Thank you.", [
            Thank(),
            And(),
            Move(done_by=DSTPronoun.I,
                 moved=DSTPronoun.I,
                 from_place=place_waiting_room,
                 to_place=places_office)
        ]),
        Utterance("So, what brings you here today?", [
            Ask(asked=Relation(left=p_problem_description, rtype=RType.IS,
                               rtense=Tense.PRESENT, negation=False,
                               right=AnyProperty()),
                negation=False,
                r_tense=Tense.PRESENT)
        ]),
        Utterance("My left eye has been red since this morning.", [
            Share(relation=Relation(
                left=p_problem_description, rtype=RType.IS, rtense=Tense.PRESENT, right=AnyProperty()
            )),
            And(),
            Share(relation=Relation(
                left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT, right=p_red
            )),
            And(),
            Share(relation=Relation(
                left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PAST, right=p_red
            ))
        ]),
        Utterance("And my vision is a little bit blurry.", [
            Share(relation=Relation(
                left=p_vision, rtype=RType.IS, rtense=Tense.PRESENT, negation=False, right=p_blurry
            ))
        ]),
        Utterance("Hm hmm...", [
            Backchannel()
        ]),
        Utterance("and it hurts a lot.", [
            Share(relation=Relation(
                left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT, negation=False,
                right=p_pain
            ))
        ]),
        Utterance("Did you take any medicine to ease your pain?", [
            Check(r_tense=Tense.PRESENT, checked=Relation(
                left=DSTPronoun.YOU, rtense=Tense.PAST, rtype=RType.ACTION, negation=False,
                right=Take(taken=p_medicine, done_by=DSTPronoun.YOU, r_tense=Tense.PRESENT, negation=False)
            ), negation=False, recipient=DSTPronoun.YOU)
        ]),
        Utterance("No, I was worried that would make it worse.", [
            Feel(done_by=DSTPronoun.I, felt=p_worry, about=Relation(
                left=DSTPronoun.I, rtense=Tense.PRESENT, rtype=RType.ACTION, negation=False,
                right=Take(r_tense=Tense.PRESENT, taken=p_medicine, done_by=DSTPronoun.I, negation=False)
            ),
                 r_tense=Tense.PAST)
        ]),
        Utterance("I see.", [
            Acknowledge()
        ]),
        Utterance("Do you have any tears?", [
            Check(checked=Relation(left=p_patients_left_eye, rtype=RType.IS,
                                   rtense=Tense.PRESENT, negation=False,
                                   right=p_teary),
                  r_tense=Tense.PRESENT,
                  negation=False,
                  recipient=DSTPronoun.YOU)
        ]),
        Utterance("Yes, both eyes.", [
            Affirm(),
            Then(),
            Share(relation=Relation(left=p_patients_left_eye, rtype=RType.IS, rtense=Tense.PRESENT,
                                    right=p_teary)),
            And(),
            Share(relation=Relation(left=p_patients_right_eye, rtype=RType.IS, rtense=Tense.PRESENT,
                                    right=p_teary))
        ]),
        Utterance("Okay, I need to examine your eye now if that's okay for you.", [
            Request(done_by=DSTPronoun.I, requested=Examine()),
            And(),
            Notify(notified_about=Relation(
                left=DSTPronoun.I, rtype=RType.ACTION, rtense=Tense.FUTURE,
                right=Examine()
            ), recipient=DSTPronoun.YOU, done_by=DSTPronoun.I)
        ]),
        Utterance("Okay.", [
            Affirm()
        ]),
        Utterance("Will it hurt?", [
            Check(r_tense=Tense.PRESENT, negation=False,
                  checked=Relation(left=Relation(left=DSTPronoun.YOU, rtype=RType.ACTION, rtense=Tense.PRESENT,
                                                 right=Examine()),
                                   rtype=RType.IS, rtense=Tense.PRESENT,
                                   right=p_painful
                                   ),
                  recipient=DSTPronoun.YOU)
        ]),
        Utterance("No, you will just feel mild pressure in your eye, but it shouldn't hurt.", [
            Deny(),
            And(),
            Share(relation=Relation(left=Relation(left=DSTPronoun.I, rtype=RType.ACTION, rtense=Tense.PRESENT,
                                                  right=Examine()),
                                    rtype=RType.IS, rtense=Tense.PRESENT,
                                    negation=True,
                                    right=p_painful
                                    ))
        ]),
        Utterance("You can tell me if it hurts or you just feel uncomfortable.", [
            When(action=Notify(recipient=DSTPronoun.I,
                               notified_about=Feel(felt=p_pain, done_by=DSTPronoun.YOU, r_tense=Tense.PRESENT,
                                                   about=Relation(left=DSTPronoun.I, rtype=RType.ACTION,
                                                                  rtense=Tense.PRESENT,
                                                                  right=Examine()))
                               , done_by=DSTPronoun.I),
                 conditions=[
                     AgentDoesAction(agent=DSTPronoun.YOU, tense=Tense.PRESENT,
                                     action=Feel(done_by=DSTPronoun.YOU, felt=p_pain, r_tense=Tense.PRESENT,
                                                 about=Relation(left=DSTPronoun.I, rtype=RType.ACTION,
                                                                rtense=Tense.PRESENT,
                                                                right=Examine())))
                 ], )
        ]),
        Utterance("Okay doctor, thank you.", [
            Acknowledge(),
            Then(),
            Thank()
        ]),
        Utterance("Can you open your eyes now?", [
            Request(requested=Open(target_resource=p_patients_both_eyes, done_by=DSTPronoun.YOU),
                    done_by=DSTPronoun.I)
        ]),
        Utterance("Perfect.", [
            Acknowledge()
        ]),
        Utterance("Let me see.", [
            SelfTalk()
        ]),
        Utterance("I see that the veins in your left eye are red.", [
            Learn(learned=Relation(left=p_veins_in_left_eye, rtype=RType.IS, rtense=Tense.PRESENT,
                                   right=p_red), done_by=DSTPronoun.I),
            And(),
            Share(relation=Relation(left=p_veins_in_left_eye, rtype=RType.IS, rtense=Tense.PRESENT,
                                    right=p_red))
        ]),
        Utterance("And there is inflammation.", [
            Learn(learned=Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                                   right=p_inflammation), done_by=DSTPronoun.I),
            And(),
            Share(relation=Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                                    right=p_inflammation))
        ]),
        Utterance("Okay.", [
            SelfTalk(),
            And(),
            Deduce(done_by=DSTPronoun.I,
                   deduced=Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                                    right=p_bacterial_conjunctivitis)),
            And(),
            Deduce(done_by=DSTPronoun.I,
                   deduced=Relation(left=p_patients_problem, rtype=RType.IS, rtense=Tense.PRESENT,
                                    right=p_bacterial_conjunctivitis))
        ]),
        Utterance("So, how is it doctor?", [
            Ask(asked=Relation(left=p_patients_problem, rtype=RType.IS, rtense=Tense.PRESENT,
                               right=AnyProperty()),
                r_tense=Tense.PRESENT),
            Or(),
            Ask(asked=Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                               right=AnyProperty()),
                r_tense=Tense.PRESENT)
        ]),
        Utterance("Your left eye has bacterial conjunctivitis.", [
            Share(relation=Relation(left=p_patients_left_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                                    right=p_bacterial_conjunctivitis))
        ]),
        Utterance("Did you have a cold recently?", [
            Check(r_tense=Tense.PRESENT, checked=Relation(
                left=DSTPronoun.YOU, rtype=RType.HAS, rtense=Tense.PAST,
                right=p_cold
            ), recipient=DSTPronoun.YOU)
        ]),
        Utterance("Yes, is that why?", [
            Affirm(),
            And(),
            Share(relation=Relation(
                left=DSTPronoun.I, rtense=Tense.PAST, rtype=RType.HAS, right=p_cold
            ))
        ]),
        Utterance("Yeah, it is pretty common to get bacterial conjunctivitis after having a cold.", [
            Share(relation=Relation(left=Relation(left=p_eye, rtype=RType.HAS, rtense=Tense.PRESENT,
                                                  right=p_bacterial_conjunctivitis), rtype=RType.IS,
                                    rtense=Tense.PRESENT,
                                    right=p_common, times=[After(after=Have(done_by=any_agent, target=p_cold))]))
        ]),
        Utterance("Oh...", [
            Acknowledge()
        ]),
        Utterance(
            "I will prescribe you some antibiotics, take them twice a day, one in the morning and one before you sleep.",
            [
                Prescribe(done_by=DSTPronoun.I, prescribed=[p_antibiotics], recipient=DSTPronoun.YOU),
                And(),
                Request(done_by=DSTPronoun.I,
                        requested=Take(done_by=DSTPronoun.YOU, taken=p_antibiotics,
                                       r_tense=Tense.PRESENT,
                                       times=[InMorning(num_of_times=NumOfTimes(1)),
                                              Before(Sleep(done_by=DSTPronoun.YOU), num_of_times=NumOfTimes(1))]
                                       ))
            ]),
        Utterance("Thank you, doctor.", [
            Thank()
        ]),
        Utterance("If it doesn't heal in a week, you can come again.", [
            When(conditions=[
                ActionOnPropertyHappens(property=p_patients_left_eye, tense=Tense.PRESENT,
                                        action=Heal(healed=p_patients_left_eye, negation=True, times=[InWeek(num=1)]))
            ],
                action=Move(done_by=DSTPronoun.YOU, moved=DSTPronoun.YOU, from_place=any_place, to_place=places_office)
            )
        ]),
        Utterance("Thank you.", [
            Thank()
        ])
    ]

    greeting_norm = Norm(name='People greet each other', action_seq=[
        Greet(), Greet()
    ],
                         skipping_conditions=[
                             AgentCanDo(agent=DSTPronoun.I, action=Greet(), tense=Tense.ANY, negation=True)
                         ],
                         completion_effects=[PromoteValue(affected=DSTPronoun.EVERYONE, value=value_politeness)],
                         violation_effects=[DemoteValue(affected=DSTPronoun.I, value=value_politeness)])
    vars.expectations.append(greeting_norm)

    session_manager.add_multi_sessions(
        [
            Session(name='Greeting',
                    start_conditions=[
                        AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=place_waiting_room),
                        AgentAtPlace(agent=agent2, tense=Tense.PRESENT, place=places_office)
                    ],
                    expectations=[
                        greeting_norm
                    ],
                    end_goals=[
                        Goal(name='Patient is ready',
                             desc='Patient and doctor greeted each other and patient is ready to talk',
                             conditions=[
                                 ExpectationStatusIs(expectation=greeting_norm,
                                                     expectation_status=ExpectationStatus.COMPLETED),
                                 AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=places_office)
                             ])
                    ]),
            Session(name='Problem Presentation',
                    start_conditions=[
                        ExpectationStatusIs(expectation=greeting_norm, expectation_status=ExpectationStatus.COMPLETED),
                        AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=places_office)
                    ],
                    end_goals=[
                        Goal(name='Patient explained the problem',
                             conditions=[
                                 AgentKnows(agent=agent2, tense=Tense.PRESENT,
                                            knows=Relation(left=p_problem_description,
                                                           rtype=RType.IS,
                                                           rtense=Tense.PRESENT,
                                                           right=AnyProperty()))
                             ])
                    ]),
            Session(name='History Taking',
                    start_conditions=[
                        AgentKnows(agent=agent2, tense=Tense.PRESENT, knows=Relation(left=p_problem_description,
                                                                                     rtype=RType.IS,
                                                                                     rtense=Tense.PRESENT,
                                                                                     right=AnyProperty()))
                    ],
                    end_goals=[
                        Goal(name='Doctor asked all the necessary questions before physical examination',
                             conditions=[
                                 AgentKnows(agent=agent2, tense=Tense.PRESENT, knows=Relation(left=p_veins_in_left_eye,
                                                                                              rtype=RType.IS,
                                                                                              rtense=Tense.PRESENT,
                                                                                              right=p_teary))
                             ])
                    ])
        ]
    )
    import logging

    logging.basicConfig(level=logging.INFO)
    # Dialogue System initialization
    ds = DialogueSystem(agents=[agent1, agent2], utterances=utterances)
    return ds


# asyncio.run(main())
