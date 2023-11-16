# from socialds.actions.action import Action
# from socialds.agent import Agent
# from socialds.dialogue_system import DialogueSystem
# from socialds.senses.sense import Sense
# # from socialpractice.activity.competence import Competence
# from socialds.socialpractice.context.actor import Actor
# from socialds.socialpractice.context.role import Role
# from socialds.socialpractice.activity.competence import Competence
#
#
#
# alex = Actor(name='Alex')
# eren = Actor(name='Eren')
#
# action_diagnose = Action(
#     name="diagnose",
#     senses=[Sense(
#         desc="diagnosing the patient to determine the cause of the patient's problem",
#         op_seq=[]
#     )])
#
# action_sit = Action(
#     name="sit",
#     senses=[Sense(
#         desc="sitting on a sittable object",
#         op_seq=[]
#     )]
# )
#
# can_diagnose = Competence(name='can diagnose', action=action_diagnose, negation=False)
# can_sit = Competence(name='can sit', action=action_sit, negation=False)
#
# role_doctor = Role(name='Doctor', competences=[can_diagnose])
# role_patient = Role(name='Patient', competences=[can_sit])
#
# doctor = Agent(actor=alex, roles=[role_doctor], resources=[], auto=False)
# patient = Agent(actor=eren, roles=[role_patient], resources=[])
#
# ds = DialogueSystem(agents=[doctor, patient])
#
# ds.run()
import socialds.simple_DST as dst
from socialds.actions.mental.feel import Feel
from socialds.actions.physical.take import Take
from socialds.actions.functional.ask import Ask
from socialds.actions.verbal.acknowledge import Acknowledge
from socialds.actions.verbal.backchannel import Backchannel
from socialds.actions.verbal.selftalk import SelfTalk
from socialds.actions.verbal.yes import Yes
from socialds.actions.verbal.thank import Thank
from socialds.actions.functional.move import Move
from socialds.actions.functional.permit import Permit
from socialds.actions.verbal.greet import Greet
from socialds.actions.functional.share import Share
from socialds.agent import Agent, any_agent
from socialds.dialogue_system import DialogueSystem
from socialds.relationstorage import RelationStorage
from socialds.repositories.action_repository import verbal_greet
from socialds.socialpractice.context.actor import Actor
from socialds.states.property import Property
from socialds.states.relation import Relation, RelationType, RelationTense
from socialds.utterance import Utterance
from socialds.socialpractice.context.place import Place

# Global properties
place_any = Place(name='any')
places_office = Place(name='office')
place_waiting_room = Place('waiting room')

# Agent 1: Joe - patient
# Agent 1's Relation Storages
agent1_kb = RelationStorage('Joe\'s Knowledgebase')
agent1_competences = RelationStorage('Joe\'s Competences')
agent1_places = RelationStorage('Joe\'s Places')
agent1_resources = RelationStorage('Joe\'s Resources')
actor1 = Actor(name="Joe", knowledgebase=RelationStorage('Actor Joe\'s Knowledgebase'))

# Agent 1's properties
p_patients_problem = Property(name="patient's problem")
p_patients_left_eye = Property(name="left_eye")
p_patients_right_eye = Property(name="right_eye")
p_sick = Property(name='sick')
p_teary = Property(name='teary')
p_healthy = Property(name='healthy')
p_blurry = Property(name='blurry')
p_vision = Property(name='vision')
p_pain = Property(name='pain')
p_red = Property(name='red')
p_worry = Property('worry')
p_medicine = Property('medicine')

# AGENT 1's relations
agent1_kb.add(Relation(
    left=actor1, r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right=p_sick))
agent1_kb.add(Relation(
    left=actor1, r_type=RelationType.HAS, r_tense=RelationTense.PRESENT, right=p_patients_left_eye))
agent1_kb.add(Relation(
    left=actor1, r_type=RelationType.HAS, r_tense=RelationTense.PRESENT, right=p_patients_right_eye))
agent1_kb.add(Relation(
    left=p_patients_left_eye, r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right=p_teary))
agent1_kb.add(Relation(
    left=p_patients_left_eye, r_type=RelationType.HAS, r_tense=RelationTense.PRESENT, right=p_pain))
agent1_kb.add(Relation(
    left=p_patients_left_eye, r_type=RelationType.HAS, r_tense=RelationTense.PRESENT, right=p_vision))
agent1_kb.add(Relation(
    left=p_vision, r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right=p_blurry))
agent1_kb.add(Relation(
    left=p_patients_right_eye, r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right=p_healthy))

# Agent 1's initialization
agent1 = Agent(name='Joe(patient)', actor=actor1, roles=[], knowledgebase=agent1_kb, competences=agent1_competences,
               places=agent1_places, resources=agent1_resources)
agent1.places.add(Relation(left=agent1, r_type=RelationType.IS_AT, r_tense=RelationTense.PRESENT,
                           right=place_any))
agent1.places.add(Relation(left=agent1, r_type=RelationType.IS_AT, r_tense=RelationTense.PRESENT,
                           right=place_waiting_room))

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

agent2.places.add(Relation(left=agent2, r_type=RelationType.IS_AT, r_tense=RelationTense.PRESENT,
                           right=place_any))

# Utterances
# utts = [
#     Utterance(text="Hi", actions=[verbal_greet()]),
#     Utterance(text="Hey!", actions=[verbal_greet()]),
#     Utterance(text="Eren is dirty!", actions=[Share(
#         Relation(left=actor1,
#                  r_type=RelationType.IS,
#                  r_tense=RelationTense.PRESENT,
#                  right=p_dirty)
#         , agent2_kb)])
# ]

utterances = [
    Utterance("Hi!", [Greet()]),
    Utterance("Hi, come in", [Greet(),
                              Permit(permitter=agent2,
                                     permitted=Relation(left=agent1, r_type=RelationType.ACTION,
                                                        r_tense=RelationTense.PRESENT, negation=False,
                                                        right=Move(mover=agent2, moved=agent2, from_place=place_any,
                                                                   to_place=places_office)),
                                     r_tense=RelationTense.PRESENT, negation=False, rs=agent2.knowledgebase)]),
    Utterance("Thank you.", [Thank()]),
    Utterance("So, what brings you here today?", [Ask(asker=agent2,
                                                      asked=Relation(left=p_patients_problem, r_type=RelationType.IS,
                                                                     r_tense=RelationTense.PRESENT, negation=False,
                                                                     right='?'),
                                                      negation=False,
                                                      r_tense=RelationTense.PRESENT,
                                                      rs=agent1.knowledgebase)]),
    Utterance("My left eye has been red since this morning.", [
        Share(relation=Relation(
            left=p_patients_left_eye, r_type=RelationType.IS, r_tense=RelationTense.PRESENT, negation=False, right=p_red
        ), rs=agent2.knowledgebase),
        Share(relation=Relation(
            left=p_patients_left_eye, r_type=RelationType.IS, r_tense=RelationTense.PAST, negation=False, right=p_red
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("And my vision is a little bit blurry.", [
        Share(relation=Relation(
            left=p_vision, r_type=RelationType.IS, r_tense=RelationTense.PRESENT, negation=False, right=p_blurry
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("Hm hmm...", [Backchannel()]),
    Utterance("and it hurts a lot.", [
        Share(relation=Relation(
            left=p_patients_left_eye, r_type=RelationType.HAS, r_tense=RelationTense.PRESENT, negation=False,
            right=p_pain
        ), rs=agent2.knowledgebase)
    ]),
    Utterance("Did you take any medicine to ease your pain?", []),
    Utterance("No, I was worried that would make it worse.", [
        Feel(felt_by=agent1, felt=p_worry, about=Relation(
            left=agent1, r_tense=RelationTense.PRESENT, r_type=RelationType.ACTION, negation=False,
            right=Take(giver=any_agent, r_tense=RelationTense.PRESENT, taken=p_medicine, taker=agent1, negation=False)
        ),
             r_tense=RelationTense.PAST)
    ]),
    Utterance("I see.", [Acknowledge()]),
    Utterance("Do you have any tears?", [
        Ask(asker=agent2,
            asked=Relation(left=p_patients_left_eye, r_type=RelationType.IS,
                           r_tense=RelationTense.PRESENT, negation=False,
                           right=p_teary),
            r_tense=RelationTense.PRESENT,
            negation=False,
            rs=agent1.knowledgebase)
    ]),
    Utterance("Yes, both eyes.", [Yes()]),
    Utterance("Okay, I need to examine your eye now if that's okay for you.", []),
    Utterance("Okay.", [Yes()]),
    Utterance("Will it hurt?", []),
    Utterance("No, you will just feel mild pressure in your eye, but it shouldn't hurt.", []),
    Utterance("You can tell me if it hurts or you just feel uncomfortable.", []),
    Utterance("Okay doctor, thank you.", [Acknowledge(), Thank()]),
    Utterance("Can you open your eyes now?", []),
    Utterance("Perfect.", [Acknowledge()]),
    Utterance("Let me see.", [SelfTalk()]),
    Utterance("I see that the veins in your eye are red.", []),
    Utterance("And there is inflammation.", []),
    Utterance("Okay.", [SelfTalk()]),
    Utterance("So, how is it doctor?", []),
    Utterance("Your left eye has bacterial conjunctivitis.", []),
    Utterance("Did you have a cold recently?", []),
    Utterance("Yes, is that why?", [Yes(), ]),
    Utterance("Yeah, it is pretty common to get bacterial conjunctivitis after having a cold.", []),
    Utterance("Oh...", [Acknowledge()]),
    Utterance("I will prescribe you some antibiotics, take them twice a day, "
              "one in the morning and one before you sleep.", []),
    Utterance("Thank you, doctor.", [Thank()]),
    Utterance("If it doesn't heal in a week, you can come again.", []),
    Utterance("Thank you.", [Thank()])
]

# Dialogue System initialization
ds = DialogueSystem(agents=[agent1, agent2], utterances=utterances)
ds.run(turns=2)
