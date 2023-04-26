from agent import Agent
from dialogue_system import DialogueSystem
from socialpractice.activitiy.competence import Competence
from socialpractice.context.actor import Actor
from socialpractice.context.role import Role

alex = Actor(name='Alex')
eren = Actor(name='Eren')

diagnose = Competence('Diagnose')
sit = Competence('Sit')

role_doctor = Role(name='Doctor', competences=[diagnose])
role_patient = Role(name='Patient', competences=[sit])

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