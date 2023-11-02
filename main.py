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
from socialds.relationstorage import RelationStorage
from socialds.agent import Agent
from socialds.dialogue_system import DialogueSystem
from socialds.repositories.action_repository import verbal_greet, op_and, physical_wave
from socialds.utterance import Utterance
from socialds.socialpractice.context.actor import Actor
from socialds.states.relation import Relation, RelationType
from socialds.socialpractice.context.info import Info


utts = [
    Utterance(text="Hi", actions=[verbal_greet()]),
    Utterance(text="Hey!", actions=[verbal_greet()])
]
actor1_kb = RelationStorage('Knowledgebase')
actor1_competences = RelationStorage('Competences')
actor1 = Actor(name="Eren", knowledgebase=actor1_kb)

info_patients_problem = Info(name="patient's problem")
info_patients_left_eye = Info(name="left eye")
info_patients_right_eye = Info(name="right eye")
actor1_kb.add(Relation(left=actor1, r_type=RelationType.IS, right='happy'))
actor1_kb.add(Relation(left=actor1, r_type=RelationType.HAS, right=info_patients_left_eye))
actor1_kb.add(Relation(left=actor1, r_type=RelationType.HAS, right=info_patients_right_eye))
actor1_kb.add(Relation(left=info_patients_left_eye, r_type=RelationType.IS, right='teary'))
actor1_kb.add(Relation(left=info_patients_right_eye, r_type=RelationType.IS, right='healthy'))

actor2_kb = RelationStorage('Knowledgebase')
actor2_competences = RelationStorage('Competences')
agent1 = Agent(actor=actor1, roles=[], competences=actor1_competences)
agent2 = Agent(actor=Actor(name="Wika", knowledgebase=actor2_kb), roles=[], competences=actor2_competences)

ds = DialogueSystem(agents=[agent1, agent2], utterances=utts)
ds.run(turns=2)

