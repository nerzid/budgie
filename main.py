from socialds.any.any_agent import AnyAgent
from socialds.any.any_place import AnyPlace
from socialds.conditions.action_happens_on_property import ActionOnPropertyHappens
from socialds.conditions.agent_at_place import AgentAtPlace
from socialds.conditions.agent_does import AgentDoes
from socialds.conditions.agent_knows import AgentKnows
from socialds.managers.managers import session_manager
from socialds.session import Session
from socialds.action.actions.functional.have import Have
from socialds.action.actiontimes.after import After
from socialds.action.actiontimes.in_morning import InMorning
from socialds.action.actions.physical.sleep import Sleep
from socialds.action.actiontimes.before import Before
from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.actions.physical.prescribe import Prescribe
from socialds.action.actionoperators.op_or import Or
from socialds.action.actions.physical.heal import Heal
from socialds.action.actiontimes.in_week import InWeek
from socialds.action.actions.functional.check import Check
from socialds.action.actions.mental.deduce import Deduce
from socialds.action.actionoperators.then import Then
from socialds.action.actionoperators.when import When
from socialds.action.actionoperators.op_and import And
from socialds.conditions.condition import Condition
from socialds.action.actions.functional.learn import Learn
from socialds.action.actions.functional.ask import Ask
from socialds.action.actions.functional.move import Move
from socialds.action.actions.functional.notify import Notify
from socialds.action.actions.functional.permit import Permit
from socialds.action.actions.functional.request import Request
from socialds.action.actions.functional.share import Share
from socialds.action.actions.mental.feel import Feel
from socialds.action.actions.physical.examine import Examine
from socialds.action.actions.physical.open import Open
from socialds.action.actions.physical.take import Take
from socialds.action.actions.verbal.acknowledge import Acknowledge
from socialds.action.actions.verbal.backchannel import Backchannel
from socialds.action.actions.verbal.greet import Greet
from socialds.action.actions.verbal.no import No
from socialds.action.actions.verbal.selftalk import SelfTalk
from socialds.action.actions.verbal.thank import Thank
from socialds.action.actions.verbal.yes import Yes
from socialds.agent import Agent
from socialds.dialogue_system import DialogueSystem
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.place import Place
from socialds.states.property import Property
from socialds.states.relation import Relation, RType
from socialds.utterance import Utterance
from socialds.enums import Tense

# Global properties
any_place = AnyPlace()
places_office = Place('office')
place_waiting_room = Place('waiting room')


any_agent = AnyAgent()
# Agent 1: Joe - patient
# Agent 1's Relation Storages
agent1_kb = RelationStorage('Joe\'s Knowledgebase')
agent1_competences = RelationStorage('Joe\'s Competences')
agent1_places = RelationStorage('Joe\'s Places')
agent1_resources = RelationStorage('Joe\'s Resources')
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

# AGENT 1's relations
agent1_kb.add_multi([
    Relation(left=actor1, r_type=RType.IS, r_tense=Tense.PRESENT, right=p_sick),
    Relation(left=actor1, r_type=RType.HAS, r_tense=Tense.PRESENT, right=p_patients_left_eye),
    Relation(left=actor1, r_type=RType.HAS, r_tense=Tense.PRESENT, right=p_patients_right_eye),
    Relation(left=p_patients_left_eye, r_type=RType.IS, r_tense=Tense.PRESENT, right=p_teary),
    Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT, right=p_pain),
    Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT, right=p_vision),
    Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
             right=p_veins_in_left_eye),
    Relation(left=p_patients_right_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
             right=p_veins_in_right_eye),
    Relation(left=p_vision, r_type=RType.IS, r_tense=Tense.PRESENT, right=p_blurry),
    Relation(left=p_patients_right_eye, r_type=RType.IS, r_tense=Tense.PRESENT, right=p_healthy)
])

# Agent 1's initialization
agent1 = Agent(name='Joe(patient)', actor=actor1, roles=[], knowledgebase=agent1_kb, competences=agent1_competences,
               places=agent1_places, resources=agent1_resources)
agent1.places.add_multi([
    Relation(left=agent1, r_type=RType.IS_AT, r_tense=Tense.PRESENT, right=any_place),
    Relation(left=agent1, r_type=RType.IS_AT, r_tense=Tense.PRESENT, right=place_waiting_room)
])

# Agent 2: Jane - doctor
# Agent 2's Relation Storages
agent2_kb = RelationStorage('Jane\'s Knowledgebase')
agent2_competences = RelationStorage('Jane\'s Competences')
agent2_places = RelationStorage('Jane\'s Places')
agent2_resources = RelationStorage('Jane\'s Resources')

# Agent 2's initialization
agent2 = Agent(name='Jane(doctor)',
               actor=Actor(name="Jane", knowledgebase=RelationStorage('Actor Jane\'s Knowledgebase ')),
               roles=[],
               knowledgebase=agent2_kb, competences=agent2_competences, places=agent2_places,
               resources=agent2_resources)

agent2.places.add_multi([
    Relation(left=agent2, r_type=RType.IS_AT, r_tense=Tense.PRESENT, right=any_place),
    Relation(left=agent2, r_type=RType.IS_AT, r_tense=Tense.PRESENT, right=places_office)
])

# Utterances
utterances = [
    Utterance("Hi!", [
        Greet()
    ]),
    Utterance("Hi, come in", [
        Greet(),
        Then(),
        Permit(permitter=agent2,
               permitted=Relation(left=agent1, r_type=RType.ACTION,
                                  r_tense=Tense.PRESENT, negation=False,
                                  right=Move(mover=agent1, moved=agent1, from_place=any_place,
                                             to_place=places_office)),
               r_tense=Tense.PRESENT, negation=False, rs=agent1.knowledgebase)
    ]),
    Utterance("Thank you.", [
        Thank(),
        And(),
        Move(mover=agent1, moved=agent1, from_place=place_waiting_room, to_place=places_office)
    ]),
    Utterance("So, what brings you here today?", [
        Ask(asker=agent2,
            asked=Relation(left=p_patients_problem, r_type=RType.IS,
                           r_tense=Tense.PRESENT, negation=False,
                           right='?'),
            negation=False,
            r_tense=Tense.PRESENT,
            rs=agent1.knowledgebase)
    ]),
    Utterance("My left eye has been red since this morning.", [
        Share(relation=Relation(
            left=p_patients_left_eye, r_type=RType.IS, r_tense=Tense.PRESENT, right=p_red
        ), rs=agent2.knowledgebase),
        And(),
        Share(relation=Relation(
            left=p_patients_left_eye, r_type=RType.IS, r_tense=Tense.PAST, right=p_red
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("And my vision is a little bit blurry.", [
        Share(relation=Relation(
            left=p_vision, r_type=RType.IS, r_tense=Tense.PRESENT, negation=False, right=p_blurry
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("Hm hmm...", [
        Backchannel()
    ]),
    Utterance("and it hurts a lot.", [
        Share(relation=Relation(
            left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT, negation=False,
            right=p_pain
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("Did you take any medicine to ease your pain?", [
        Check(checker=agent2, r_tense=Tense.PRESENT, checked=Relation(
            left=agent1, r_tense=Tense.PAST, r_type=RType.ACTION, negation=False,
            right=Take(taken=p_medicine, taker=agent1, r_tense=Tense.PRESENT, negation=False)
        ), negation=False, checked_rs=agent2.knowledgebase)
    ]),
    Utterance("No, I was worried that would make it worse.", [
        Feel(felt_by=agent1, felt=p_worry, about=Relation(
            left=agent1, r_tense=Tense.PRESENT, r_type=RType.ACTION, negation=False,
            right=Take(r_tense=Tense.PRESENT, taken=p_medicine, taker=agent1, negation=False)
        ),
             r_tense=Tense.PAST)
    ]),
    Utterance("I see.", [
        Acknowledge()
    ]),
    Utterance("Do you have any tears?", [
        Check(checker=agent2,
              checked=Relation(left=p_patients_left_eye, r_type=RType.IS,
                               r_tense=Tense.PRESENT, negation=False,
                               right=p_teary),
              r_tense=Tense.PRESENT,
              negation=False,
              checked_rs=agent1.knowledgebase)
    ]),
    Utterance("Yes, both eyes.", [
        Yes(),
        Then(),
        Share(relation=Relation(left=p_patients_left_eye, r_type=RType.IS, r_tense=Tense.PRESENT,
                                right=p_teary), rs=agent2.knowledgebase),
        And(),
        Share(relation=Relation(left=p_patients_right_eye, r_type=RType.IS, r_tense=Tense.PRESENT,
                                right=p_teary), rs=agent2.knowledgebase)
    ]),
    Utterance("Okay, I need to examine your eye now if that's okay for you.", [
        Request(requester=agent2, requested=Relation(
            left=agent2, r_type=RType.ACTION, r_tense=Tense.PRESENT,
            right=Examine()
        )),
        And(),
        Notify(notifier=agent2, notified_about=Relation(
            left=agent2, r_type=RType.ACTION, r_tense=Tense.FUTURE,
            right=Examine()
        ), notified_to=agent1)
    ]),
    Utterance("Okay.", [
        Yes()
    ]),
    Utterance("Will it hurt?", [
        Check(checker=agent1, r_tense=Tense.PRESENT, negation=False,
              checked=Relation(left=Relation(left=agent2, r_type=RType.ACTION, r_tense=Tense.PRESENT,
                                             right=Examine()),
                               r_type=RType.IS, r_tense=Tense.PRESENT,
                               right=p_painful
                               ), checked_rs=agent2.knowledgebase)
    ]),
    Utterance("No, you will just feel mild pressure in your eye, but it shouldn't hurt.", [
        No(),
        And(),
        Share(relation=Relation(left=Relation(left=agent2, r_type=RType.ACTION, r_tense=Tense.PRESENT,
                                              right=Examine()),
                                r_type=RType.IS, r_tense=Tense.PRESENT,
                                negation=True,
                                right=p_painful
                                ), rs=agent1.knowledgebase)

    ]),
    Utterance("You can tell me if it hurts or you just feel uncomfortable.", [
        When(action=Notify(notifier=agent1, notified_to=agent2,
                           notified_about=Relation(
                               left=agent1, r_type=RType.ACTION, r_tense=Tense.PRESENT,
                               right=Feel(felt=p_pain, felt_by=agent1, r_tense=Tense.PRESENT,
                                          about=Relation(left=agent2, r_type=RType.ACTION,
                                                         r_tense=Tense.PRESENT,
                                                         right=Examine()))
                           )),
             conditions=[
                 # Condition(
                 #     relation=Relation(
                 #         left=Relation(left=agent2, r_type=RType.ACTION, r_tense=Tense.PRESENT,
                 #                       right=Examine()),
                 #         r_type=RType.IS,
                 #         r_tense=Tense.PRESENT,
                 #         right=p_painful
                 #     ))
                 AgentDoes(agent=agent1, tense=Tense.PRESENT,
                           action=Feel(felt_by=agent1, felt=p_pain, r_tense=Tense.PRESENT,
                                       about=Relation(left=agent2, r_type=RType.ACTION,
                                                      r_tense=Tense.PRESENT,
                                                      right=Examine())))
             ], )
    ]),
    Utterance("Okay doctor, thank you.", [
        Acknowledge(),
        Then(),
        Thank()
    ]),
    Utterance("Can you open your eyes now?", [
        Request(requester=agent2, requested=Relation(
            left=agent1, r_type=RType.ACTION, r_tense=Tense.PRESENT, negation=False,
            right=Open(target=p_patients_both_eyes, by=agent1)
        ))
    ]),
    Utterance("Perfect.", [
        Acknowledge()
    ]),
    Utterance("Let me see.", [
        SelfTalk()
    ]),
    Utterance("I see that the veins in your left eye are red.", [
        Learn(learner=agent2,
              learned=Relation(left=p_veins_in_left_eye, r_type=RType.IS, r_tense=Tense.PRESENT,
                               right=p_red)),
        And(),
        Share(relation=Relation(left=p_veins_in_left_eye, r_type=RType.IS, r_tense=Tense.PRESENT,
                                right=p_red),
              rs=agent1.knowledgebase)
    ]),
    Utterance("And there is inflammation.", [
        Learn(learner=agent2,
              learned=Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
                               right=p_inflammation)),
        And(),
        Share(relation=Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
                                right=p_inflammation),
              rs=agent1.knowledgebase)
    ]),
    Utterance("Okay.", [
        SelfTalk(),
        And(),
        Deduce(deducer=agent2,
               deduced=Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
                                right=p_bacterial_conjunctivitis)),
        And(),
        Deduce(deducer=agent2,
               deduced=Relation(left=p_patients_problem, r_type=RType.IS, r_tense=Tense.PRESENT,
                                right=p_bacterial_conjunctivitis))
    ]),
    Utterance("So, how is it doctor?", [
        Ask(asker=agent1,
            asked=Relation(left=p_patients_problem, r_type=RType.IS, r_tense=Tense.PRESENT,
                           right='?'),
            r_tense=Tense.PRESENT,
            rs=agent2.knowledgebase),
        Or(),
        Ask(asker=agent1,
            asked=Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
                           right='?'),
            r_tense=Tense.PRESENT,
            rs=agent2.knowledgebase)
    ]),
    Utterance("Your left eye has bacterial conjunctivitis.", [
        Share(relation=Relation(left=p_patients_left_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
                                right=p_bacterial_conjunctivitis), rs=agent1.knowledgebase)
    ]),
    Utterance("Did you have a cold recently?", [
        Check(checker=agent2, r_tense=Tense.PRESENT, checked=Relation(
            left=agent1, r_type=RType.HAS, r_tense=Tense.PAST,
            right=p_cold
        ), checked_rs=agent1.knowledgebase)
    ]),
    Utterance("Yes, is that why?", [
        Yes(),
        And(),
        Share(relation=Relation(
            left=agent1, r_tense=Tense.PAST, r_type=RType.HAS, right=p_cold
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("Yeah, it is pretty common to get bacterial conjunctivitis after having a cold.", [
        Share(relation=Relation(left=Relation(left=p_eye, r_type=RType.HAS, r_tense=Tense.PRESENT,
                                              right=p_bacterial_conjunctivitis), r_type=RType.IS,
                                r_tense=Tense.PRESENT,
                                right=p_common, times=[After(after=Have(owner=any_agent, target=p_cold))]),
              rs=agent1.knowledgebase)
    ]),
    Utterance("Oh...", [
        Acknowledge()
    ]),
    Utterance(
        "I will prescribe you some antibiotics, take them twice a day, one in the morning and one before you sleep.", [
            Prescribe(prescriber=agent2, prescribed=[p_antibiotics], prescribed_for=agent1),
            And(),
            Request(requester=agent2,
                    requested=Relation(left=agent1, r_type=RType.ACTION, r_tense=Tense.FUTURE,
                                       right=Take(taker=agent1, taken=p_antibiotics,
                                                  r_tense=Tense.PRESENT,
                                                  times=[InMorning(num_of_times=NumOfTimes(1)),
                                                         Before(Sleep(sleeper=agent1), num_of_times=NumOfTimes(1))])))
        ]),
    Utterance("Thank you, doctor.", [
        Thank()
    ]),
    Utterance("If it doesn't heal in a week, you can come again.", [
        When(conditions=[
            # Condition(
            #     relation=Relation(left=p_patients_left_eye, r_tense=Tense.PRESENT, r_type=RType.ACTION,
            #                       right=Heal(healed=p_patients_left_eye, negation=True, times=[InWeek(num=1)])))
            ActionOnPropertyHappens(property=p_patients_left_eye, tense=Tense.PRESENT,
                                    action=Heal(healed=p_patients_left_eye, negation=True, times=[InWeek(num=1)]))
        ],
            action=Move(mover=agent1, moved=agent1, from_place=any_place, to_place=places_office)
        )
    ]),
    Utterance("Thank you.", [
        Thank()
    ])
]

session_manager.add_multi_sessions(
    [
        Session(name='Greeting',
                start_conditions=[
                    AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=place_waiting_room),
                    AgentAtPlace(agent=agent2, tense=Tense.PRESENT, place=places_office)
                ],
                end_conditions=[
                    AgentDoes(agent=any_agent, tense=Tense.PAST, action=Greet(), times=[NumOfTimes(2)]),
                    AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=places_office)
                ]),
        Session(name='Problem Presentation',
                start_conditions=[
                    AgentDoes(agent=any_agent, tense=Tense.PAST, action=Greet(), times=[NumOfTimes(2)]),
                    AgentAtPlace(agent=agent1, tense=Tense.PRESENT, place=places_office)
                ],
                end_conditions=[
                    AgentKnows(agent=agent2, tense=Tense.PRESENT, knows=Relation(left=p_patients_left_eye,
                                                                                 r_type=RType.IS,
                                                                                 r_tense=Tense.PRESENT,
                                                                                 right=p_red))
                ]),
        Session(name='History Taking',
                start_conditions=[
                    AgentKnows(agent=agent2, tense=Tense.PRESENT, knows=Relation(left=p_patients_left_eye,
                                                                                 r_type=RType.IS,
                                                                                 r_tense=Tense.PRESENT,
                                                                                 right=p_red))
                ],
                end_conditions=[
                    AgentKnows(agent=agent2, tense=Tense.PRESENT, knows=Relation(left=p_veins_in_left_eye,
                                                                                 r_type=RType.IS,
                                                                                 r_tense=Tense.PRESENT,
                                                                                 right=p_teary))
                ])
    ]
)

# Dialogue System initialization
ds = DialogueSystem(agents=[agent1, agent2], utterances=utterances)
ds.run(turns=2)
