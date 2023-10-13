from actions.action import Action
from agent import Agent
from definitions.definition import Definition
from dialogue_system import DialogueSystem
# from socialpractice.activity.competence import Competence
from socialpractice.context.actor import Actor
from socialpractice.context.role import Role
from states.competence import Competence

alex = Actor(name='Alex')
eren = Actor(name='Eren')


diagnose = Action(name="diagnose", denotations=[Definition(
    desc="diagnosing the patient to determine the cause of the patient's problem",

)])

can_diagnose = Competence(action=Action())
can_sit = Competence('Sit')

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
print("test123215")