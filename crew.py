import os
import re
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLMs
llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.environ.get("GOOGLE_API_KEY"))
planning_llm = LLM(model="gemini/gemini-2.0-flash-thinking-exp-01-21", api_key=os.environ.get("GOOGLE_API_KEY"))

# Utility function to clean filenames
def clean_filename(text: str) -> str:
    if not text or not isinstance(text, str):
        raise ValueError("Invalid topic. Please provide a non-empty string.")
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_") + ".html"

# Pydantic Models for Story Data
class Citation(BaseModel):
    title: str = Field(description="Title of the source")
    url: str = Field(description="URL of the source")
    context: str = Field(description="Brief context of why this source is relevant")

class Character(BaseModel):
    name: str = Field(description="Character's name")
    role: str = Field(description="Character's role in the story")
    description: str = Field(description="Brief description of the character")
    motivation: str = Field(description="Character's primary motivation")
    cultural_significance: Optional[str] = Field(None, description="Cultural significance of this character")

class StoryResearch(BaseModel):
    citations: List[Citation] = Field(default_factory=list, description="Sources used in research")
    cultural_context: str = Field(description="Cultural insights and background information")
    historical_context: Optional[str] = Field(None, description="Historical setting and relevance")
    key_themes: List[str] = Field(default_factory=list, description="Main themes identified in research")

class StoryPlan(BaseModel):
    title: str = Field(description="Title of the story")
    characters: List[Dict[str, str]] = Field(default_factory=list, description="Characters in the story")
    plot_points: List[str] = Field(default_factory=list, description="Key events in sequential order")
    setting: str = Field(description="Time period and location details")
    theme: str = Field(description="Central theme of the story")
    cultural_elements: List[str] = Field(default_factory=list, description="Cultural elements to include")

class StoryDraft(BaseModel):
    title: str = Field(description="Title of the story")
    content: str = Field(description="Full text of the story")
    citations_used: List[Citation] = Field(default_factory=list, description="Citations used in the story")

class ConsistencyReview(BaseModel):
    is_consistent: bool = Field(description="Whether the story is consistent")
    issues: List[str] = Field(default_factory=list, description="Identified consistency issues")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    cultural_accuracy: str = Field(description="Assessment of cultural accuracy")

@CrewBase
class StoryTellingCrew:
    """A Crew that generates a culturally authentic story and saves it as an HTML file."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, topic: str, file_topic: Optional[str] = None):
        if not topic or not isinstance(topic, str):
            raise ValueError("Invalid topic. Please provide a non-empty string.")
        self.topic = topic
        self.file_topic = file_topic if file_topic else topic

    # **Agents**
    @agent
    def story_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["story_manager"],
            llm=llm,
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            max_rpm=40,
            cache=True,
        )

    @agent
    def story_planner(self) -> Agent:
        return Agent(config=self.agents_config["story_planner"], llm=llm, verbose=True)

    @agent
    def background_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["background_researcher"],
            tools=[SerperDevTool()],
            llm=llm,
            verbose=True,
        )

    @agent
    def cultural_expert(self) -> Agent:
        return Agent(config=self.agents_config["cultural_expert"], llm=llm, verbose=True)

    @agent
    def consistency_checker(self) -> Agent:
        return Agent(config=self.agents_config["consistency_checker"], llm=llm, verbose=True)

    @agent
    def story_writer(self) -> Agent:
        return Agent(config=self.agents_config["story_writer"], llm=llm, verbose=True)

    @agent
    def web_designer(self) -> Agent:
        return Agent(config=self.agents_config["web_designer"], llm=llm, verbose=True)

    # **Tasks**
    @task
    def search_and_gather_story_data(self) -> Task:
        search_input = {"search_query": f"{self.topic}, historical sources, cultural analysis"}
        return Task(
            config=self.tasks_config["search_and_gather_story_data"],
            agent=self.background_researcher(),
            input_template=search_input,
            output_pydantic=StoryResearch,
        )

    @task
    def analyze_cultural_context(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_cultural_context"],
            agent=self.cultural_expert(),
            input_models={"research": StoryResearch},
            output_template={"cultural_analysis": "Detailed cultural context and authenticity guidelines"},
        )

    @task
    def plan_story(self) -> Task:
        return Task(
            config=self.tasks_config["plan_story"],
            agent=self.story_planner(),
            input_models={"research": StoryResearch},
            output_pydantic=StoryPlan,
        )

    @task
    def write_story(self) -> Task:
        return Task(
            config=self.tasks_config["write_story"],
            agent=self.story_writer(),
            input_models={"research": StoryResearch, "plan": StoryPlan},
            output_pydantic=StoryDraft,
        )

    @task
    def ensure_narrative_consistency(self) -> Task:
        return Task(
            config=self.tasks_config["ensure_narrative_consistency"],
            agent=self.consistency_checker(),
            input_models={"draft": StoryDraft, "plan": StoryPlan, "research": StoryResearch},
            output_pydantic=ConsistencyReview,
        )

    @task
    def generate_story_html_task(self) -> Task:
        filename = clean_filename(self.file_topic)
        output_path = f"assets/{filename}"
        return Task(
            config=self.tasks_config["generate_story_html"],
            agent=self.web_designer(),
            input_models={
                "draft": StoryDraft,
                "review": ConsistencyReview,
                "citations": List[Citation]  # Add this line
            },
            output_file=output_path,
            output_template={
                "html_content": "Complete HTML document with embedded CSS, JavaScript, and citations"
            }
        )

    # **Create Crew with Sequential Process**
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.story_planner(),
                self.background_researcher(),
                self.cultural_expert(),
                self.consistency_checker(),
                self.story_writer(),
                self.web_designer()
            ],
            tasks=[
                self.search_and_gather_story_data(),
                self.analyze_cultural_context(),
                self.plan_story(),
                self.write_story(),
                self.ensure_narrative_consistency(),
                self.generate_story_html_task()
            ],
            manager_agent=self.story_manager(),
            # process=Process.hierarchical,
            planning=True,
            planning_llm=planning_llm,
            respect_context_window=True,
            verbose=True,
        )

# **Execution**
if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)

    topic = "Ram and Ravan Fight in Ramayana"
    inputs = {"topic": topic}

    try:
        story_crew = StoryTellingCrew(topic)
        result = story_crew.crew().kickoff(inputs=inputs)

        output_filename = f"assets/{clean_filename(topic)}"
        print(f"✅ Story saved at: {output_filename}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()