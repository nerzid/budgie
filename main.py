from socialds.actions.action import Action
from socialds.agent import Agent
from socialds.dialogue_system import DialogueSystem
from socialds.senses.sense import Sense
# from socialpractice.activity.competence import Competence
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role
from socialds.socialpractice.activity.competence import Competence

alex = Actor(name='Alex')
eren = Actor(name='Eren')

action_diagnose = Action(
    name="diagnose",
    senses=[Sense(
        desc="diagnosing the patient to determine the cause of the patient's problem",
        op_seq=[]
    )])

action_sit = Action(
    name="sit",
    senses=[Sense(
        desc="sitting on a sittable object",
        op_seq=[]
    )]
)

can_diagnose = Competence(name='can diagnose', action=action_diagnose, negation=False)
can_sit = Competence(name='can sit', action=action_sit, negation=False)

role_doctor = Role(name='Doctor', competences=[can_diagnose])
role_patient = Role(name='Patient', competences=[can_sit])

doctor = Agent(actor=alex, roles=[role_doctor], resources=[], auto=False)
patient = Agent(actor=eren, roles=[role_patient], resources=[])

ds = DialogueSystem(agents=[doctor, patient])

ds.run()

print("test3")
print("test5")

print("test3")
print("test52")
print("test3")
print("test12321s2sssss5ss")
