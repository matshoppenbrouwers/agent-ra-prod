from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import List
from ...models import Framework  # Import shared Framework model

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class ProductFeature(BaseModel):
	name: str
	description: str
	framework: Framework

class TechnicalRequirement(BaseModel):
	name: str 
	description: str
	framework: Framework

class BlogContentPlan(BaseModel):
    framework: Framework
    core_concepts: str
    target_audience: str
    key_principles: str
    scientific_backing: str
    implementation_guide: str
    case_studies: str
    challenges_solutions: str
    distribution_strategy: str

class BlogPlan(BaseModel):
    frameworks: List[Framework]
    content_plans: List[BlogContentPlan]
    timestamp: str

class ProductImplementationPlan(BaseModel):
    framework: Framework
    core_principles_implementation: str
    essential_features: List[ProductFeature]
    technical_requirements: List[TechnicalRequirement]
    user_experience: str
    development_roadmap: str
    implementation_challenges: str
    resource_requirements: str
    success_metrics: str

class ProductDesignPlan(BaseModel):
    implementation_plans: List[ProductImplementationPlan]
    timestamp: str

@CrewBase
class EduPlanning():
	"""EduPlanning crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def blog_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['blog_planner'],
			verbose=True
		)

	@agent
	def design_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['design_planner'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def blog_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['blog_planning_task'],
			output_file='output/blog_plan.md',
			output_pydantic=BlogPlan,
		)

	@task
	def product_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['product_planning_task'],
			output_file='output/product_plan.md',
			output_pydantic=ProductDesignPlan,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the EduPlanning crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
