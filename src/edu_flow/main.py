#!/usr/bin/env python
import os
import warnings
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace
from datetime import datetime
from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start
from .crews.edu_research.edu_research import EduResearch
from .crews.edu_planning.edu_planning import EduPlanning
from .crews.edu_writing.edu_writing import EduWriting

# Load environment variables and initialize langtrace
load_dotenv()

api_key = os.getenv('LANGTRACE_API_KEY')
langtrace.init(api_key=api_key)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

class EduFlow(Flow):

    def __init__(self):
        super().__init__()
        # Initialize langtrace if API key is available
        if api_key:
            langtrace.init(api_key=api_key)
        else:
            warnings.warn("LANGTRACE_API_KEY not found in environment variables")
        
        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)

    @start()
    def generate_researched_content(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        inputs = {
            "topic": "Productivity Frameworks in Popular Science",
            "timestamp": timestamp
        }
        try:
            crew_output = EduResearch().crew().kickoff(inputs)
            return crew_output.pydantic
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise e
        
    @listen(generate_researched_content)
    def generate_planning(self, research_output):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Set up logging to file
        log_file = os.path.join('output', 'flow_debug.log')
        with open(log_file, 'a') as f:
            f.write(f"\n\n=== New Flow Run at {timestamp} ===\n")
            
            # Log research output
            f.write(f"\n=== Research Output ===\n")
            f.write(f"Number of frameworks: {len(research_output.frameworks)}\n")
            for i, framework in enumerate(research_output.frameworks):
                f.write(f"\nFramework {i+1}:\n")
                f.write(f"Name: {framework.name}\n")
                f.write(f"Description: {framework.description}\n")
                f.write(f"Scientific Basis: {framework.scientific_basis}\n")
                f.write(f"Key Proponents: {', '.join(framework.key_proponents)}\n")
                f.write(f"Practical Applications: {', '.join(framework.practical_applications)}\n")
                f.write(f"Implementation Requirements: {', '.join(framework.implementation_requirements)}\n")
                f.write(f"Limitations: {', '.join(framework.limitations)}\n")
        
        inputs = {
            "topic": "Personal Productivity Frameworks",
            "frameworks": research_output.frameworks,
            "timestamp": timestamp
        }
        final_blog_content = []
        for framework in inputs['frameworks']:
            planner_inputs = inputs.copy()
            framework_json = framework.model_dump_json()
            
            # Log what's being sent to planners
            with open(log_file, 'a') as f:
                f.write(f"\n=== Sending to Planning Crew ===\n")
                f.write(f"Framework JSON: {framework_json}\n")
            
            planner_inputs['framework'] = framework_json
            try:
                planning_output = EduPlanning().crew().kickoff(planner_inputs)
                # Log planning output
                with open(log_file, 'a') as f:
                    f.write(f"\n=== Planning Output ===\n")
                    f.write(f"Output type: {type(planning_output)}\n")
                    f.write(f"Output content: {str(planning_output)[:500]}...\n")
                final_blog_content.append(planning_output)
            except Exception as e:
                with open(log_file, 'a') as f:
                    f.write(f"\n=== Planning Error ===\n")
                    f.write(f"Error: {str(e)}\n")
                raise e
            
        return final_blog_content
        
    @listen(generate_planning)
    def generate_blog_content(self, crew_outputs):
        # Use the product_plan from blog writing crew
            pass
        

    @listen(generate_planning)
    def generate_product_specs(self, crew_outputs):
        # Use the product_plan from product spec crew
            pass


def kickoff():
    edu_flow = EduFlow()
    edu_flow.kickoff()

def plot():
    edu_flow = EduFlow()
    edu_flow.plot()

if __name__ == "__main__":
    kickoff()
