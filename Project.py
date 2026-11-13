from dataclasses import dataclass
import random
from drafter import *
from bakery import assert_equal


# ---------------------------------------------------------------------------
# Site Information (Update with your own details before deploying to GitHub)
# ---------------------------------------------------------------------------
set_site_information(
    author="loganwo@udel.edu",
    description=(
        "Beyond the Temperature: An interactive educational website teaching "
        "people about the lesser-known effects of climate change on food, "
        "sleep, and disease-carrying insects."
    ),
    sources=[
        "IPCC Climate Change Reports",
        "NASA Global Climate Change Vital Signs",
    ],
    planning=["final_project_design.pdf"],
    links=["https://github.com/loganwo07/CISC106FinalProject.git"],
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
@dataclass
class ClimateFact:
    """Represents a single climate change fact, explanation, and solution."""
    topic: str
    fact: str
    explanation: str
    solution: str


@dataclass
class State:
    """Tracks the user's current topic, active fact, views, fact list, and feedback."""
    current_topic: str
    current_fact: ClimateFact
    facts_viewed: int
    climate_facts: list[ClimateFact]
    feedback_message: str


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def create_default_facts() -> list[ClimateFact]:
    """Creates and returns the initial list of ClimateFact instances."""
    return [
        ClimateFact(
            "Food",
            "Suitable land for growing coffee could drop by 50% by 2050.",
            "Coffee plants are highly sensitive to rising temperatures and "
            "changing rainfall patterns in tropical regions.",
            "Buy shade-grown, fair-trade coffee and reduce food waste.",
        ),
        ClimateFact(
            "Food",
            "Cacao trees face severe drought stress in West Africa.",
            "Over 70% of the world's cocoa is grown in West Africa, where "
            "longer dry seasons shrink harvest yields.",
            "Support sustainable cocoa farming initiatives and plant-rich diets.",
        ),
        ClimateFact(
            "Sleep",
            "Warm nights erode an average of 44 hours of sleep per person yearly.",
            "The human body needs to cool down at night to enter deep sleep, "
            "and elevated nighttime temperatures disrupt this process.",
            "Use breathable bedding, fans, and support urban tree canopies.",
        ),
        ClimateFact(
            "Insects",
            "Mosquito seasons have lengthened in over 75% of U.S. cities.",
            "Warmer, wetter springs and falls create longer breeding windows "
            "for mosquitoes carrying dengue and West Nile virus.",
            "Eliminate standing water around homes and use window screens.",
        ),
        ClimateFact(
            "Oceans",
            "Oceans absorb about 90% of the excess heat trapped by emissions.",
            "Warming ocean waters cause coral bleaching and shift marine "
            "food webs poleward.",
            "Reduce single-use plastics and lower household energy consumption.",
        ),
    ]


def create_initial_state() -> State:
    """Creates the starting State for the application and unit tests."""
    default_facts = create_default_facts()
    return State(
        current_topic="Home",
        current_fact=default_facts[0],
        facts_viewed=1,
        climate_facts=default_facts,
        feedback_message="No feedback submitted yet.",
    )


def format_all_facts(facts: list[ClimateFact]) -> list[str]:
    """Iterates over the ClimateFact list and formats each fact as a string."""
    formatted_list: list[str] = []
    for item in facts:
        entry = (
            "[" + item.topic + "] " + item.fact
            + " — Action: " + item.solution
        )
        formatted_list.append(entry)
    return formatted_list


def build_topic_feedback(
    user_name: str, selected_topic: str, pledge_checked: bool
) -> str:
    """Builds a custom thank-you message using conditionals on user inputs."""
    clean_name = user_name.strip()
    if clean_name == "":
        greeting = "Thank you, Climate Explorer!"
    else:
        greeting = "Thank you, " + clean_name + "!"

    if selected_topic == "Food":
        topic_msg = (
            " We are glad you enjoyed the Food section! Protecting crops "
            "like coffee and cocoa starts with sustainable agriculture."
        )
    elif selected_topic == "Sleep":
        topic_msg = (
            " We are glad you enjoyed the Sleep section! Cooler cities and "
            "green spaces help everyone rest better at night."
        )
    else:
        topic_msg = (
            " We are glad you enjoyed the Insects section! Managing standing "
            "water helps keep communities safe from vector-borne illness."
        )

    if pledge_checked:
        pledge_msg = (
            " Thank you for committing to share a climate fact with a friend!"
        )
    else:
        pledge_msg = (
            " Consider sharing one fact you learned today with a friend!"
        )

    return greeting + topic_msg + pledge_msg


def get_milestone_banner(facts_viewed: int) -> str:
    """Returns a congratulatory message once the user views at least 5 facts."""
    if facts_viewed >= 5:
        return (
            "🌟 Wow, you're a climate expert! You've read "
            + str(facts_viewed)
            + " facts."
        )
    return (
        "Facts explored so far: "
        + str(facts_viewed)
        + " (View 5 facts to unlock Climate Expert status!)"
    )


# ---------------------------------------------------------------------------
# Routes (8 Total Routes, 5+ Distinct Pages)
# ---------------------------------------------------------------------------
@route
def index(state: State) -> Page:
    """Default landing route that directs visitors to the home page."""
    return home(state)


@route
def home(state: State) -> Page:
    """Displays the Home Page with navigation buttons and the feedback form."""
    state.current_topic = "Home"
    return Page(
        state,
        [
            Header("Beyond the Temperature", 1),
            "Explore the lesser-known effects of human-driven climate change "
            "on everyday life, from your morning coffee to your nightly sleep.",
            HorizontalRule(),
            Header("Explore a Climate Topic", 2),
            Button("Food & Agriculture", "food_page"),
            Button("Sleep & Health", "sleep_page"),
            Button("Disease & Insects", "insects_page"),
            Button("Climate Fact Explorer", "fact_page"),
            HorizontalRule(),
            Header("Share Your Feedback & Take the Pledge", 2),
            "Your Name:",
            TextBox("user_name", ""),
            "Which topic was your favorite?",
            SelectBox("selected_topic", ["Food", "Sleep", "Insects"], "Food"),
            "I pledge to share one climate fact with a friend:",
            CheckBox("pledge_checked", False),
            Button("Submit Feedback", "submit_feedback"),
            HorizontalRule(),
            "Latest Community Response: " + state.feedback_message,
        ],
    )


@route
def food_page(state: State) -> Page:
    """Displays the Food and Agriculture Page with stats and solutions."""
    state.current_topic = "Food"
    return Page(
        state,
        [
            Header("How Climate Change Affects Food & Agriculture", 1),
            Header("Key Statistics", 2),
            BulletedList([
                "Up to 50% of current coffee-growing land may become "
                "unsuitable by 2050 due to rising heat.",
                "Cacao-growing regions in West Africa face increasing heat "
                "waves and unpredictable rainfall.",
                "Pollinator activity drops during extreme temperature spikes, "
                "reducing fruit and vegetable yields.",
            ]),
            Header("Why Is This Happening?", 2),
            "Crops like coffee and chocolate require narrow temperature and "
            "moisture ranges. As global temperatures rise and droughts become "
            "more frequent, farmers must either move crops upslope or switch "
            "to heat-tolerant varieties.",
            Header("What Can We Do?", 2),
            BulletedList([
                "Reduce household food waste by planning meals ahead.",
                "Choose shade-grown and sustainably certified coffee and cocoa.",
                "Support local farmers and diversify plant-based meals.",
            ]),
            HorizontalRule(),
            Button("Explore Random Climate Facts", "fact_page"),
            Button("Back to Home", "home"),
        ],
    )


@route
def sleep_page(state: State) -> Page:
    """Displays the Sleep and Health Page explaining nighttime heat impacts."""
    state.current_topic = "Sleep"
    return Page(
        state,
        [
            Header("Climate Change and Sleep Health", 1),
            Header("Key Statistics", 2),
            BulletedList([
                "Nighttime temperatures are rising faster than daytime "
                "temperatures in many urban areas.",
                "Adults lose an average of 44 hours of sleep per year due to "
                "suboptimal nighttime temperatures.",
                "By 2099, warmer nights could cause 50 to 58 hours of lost "
                "sleep per person annually.",
            ]),
            Header("How Heat Disrupts Sleep", 2),
            "To fall asleep and stay in restorative deep sleep, your core "
            "body temperature needs to drop by about 1 to 2 degrees "
            "Fahrenheit. Warm, humid nights prevent heat from escaping the "
            "body, leading to fragmented and shorter sleep.",
            Header("Ways to Protect Yourself & Your Community", 2),
            BulletedList([
                "Keep blinds closed during the sunny afternoon to trap cool air.",
                "Use breathable cotton or linen bedding and fans for airflow.",
                "Advocate for urban tree planting to reduce the heat-island effect.",
            ]),
            HorizontalRule(),
            Button("Explore Random Climate Facts", "fact_page"),
            Button("Back to Home", "home"),
        ],
    )


@route
def insects_page(state: State) -> Page:
    """Displays the Disease and Insects Page covering mosquito habitats."""
    state.current_topic = "Insects"
    return Page(
        state,
        [
            Header("Climate Change and Disease-Carrying Insects", 1),
            Header("Key Statistics", 2),
            BulletedList([
                "Mosquito-friendly days have increased in over 75% of U.S. "
                "cities over the past four decades.",
                "Ticks are expanding their geographic range northward as "
                "winters become shorter and milder.",
                "Warmer temperatures speed up the incubation of viruses like "
                "dengue and West Nile inside mosquitoes.",
            ]),
            Header("Why Changing Weather Expands Insect Habitats", 2),
            "Insects are cold-blooded, meaning their reproduction and biting "
            "rates depend directly on ambient temperatures. Heavier downpours "
            "combined with warmer autumn months create ideal stagnant-water "
            "breeding grounds.",
            Header("How to Protect Yourself", 2),
            BulletedList([
                "Tip and toss standing water from plant saucers and gutters.",
                "Repair window and door screens before warmer months arrive.",
                "Wear EPA-registered insect repellent when hiking or gardening.",
            ]),
            HorizontalRule(),
            Button("Explore Random Climate Facts", "fact_page"),
            Button("Back to Home", "home"),
        ],
    )


@route
def fact_page(state: State) -> Page:
    """Displays the Climate Fact Explorer Page, random generator, and full list."""
    state.current_topic = "Fact Explorer"
    milestone_text = get_milestone_banner(state.facts_viewed)
    all_facts_items = format_all_facts(state.climate_facts)

    return Page(
        state,
        [
            Header("Climate Fact Explorer", 1),
            milestone_text,
            HorizontalRule(),
            Header("Featured Climate Fact (" + state.current_fact.topic + ")", 2),
            "Fact: " + state.current_fact.fact,
            "Why it matters: " + state.current_fact.explanation,
            "What you can do: " + state.current_fact.solution,
            Button("Another Fact", "another_fact"),
            HorizontalRule(),
            Header("Contribute a New Climate Fact to the Collection", 2),
            "Topic (e.g., Food, Sleep, Insects, Oceans):",
            TextBox("new_topic", "Food"),
            "Climate Fact:",
            TextBox("new_fact", ""),
            "Brief Solution:",
            TextBox("new_solution", ""),
            Button("Add Fact to Collection", "add_custom_fact"),
            HorizontalRule(),
            Header("All Climate Facts in Our Collection", 2),
            BulletedList(all_facts_items),
            Button("Back to Home", "home"),
        ],
    )


@route
def another_fact(state: State) -> Page:
    """Selects a random ClimateFact and increments facts_viewed.

    Note on Unit Testing: This route uses random.choice() to pick a random
    ClimateFact from state.climate_facts, so it is non-deterministic and
    cannot be unit tested with a fixed expected output.
    """
    state.current_fact = random.choice(state.climate_facts)
    state.facts_viewed = state.facts_viewed + 1
    return fact_page(state)


@route
def add_custom_fact(
    state: State, new_topic: str, new_fact: str, new_solution: str
) -> Page:
    """Adds a user-contributed ClimateFact to state.climate_facts."""
    clean_fact = new_fact.strip()
    clean_solution = new_solution.strip()
    clean_topic = new_topic.strip()

    if clean_topic == "":
        clean_topic = "General"
    if clean_solution == "":
        clean_solution = "Share awareness with your local community."

    if clean_fact != "":
        created_fact = ClimateFact(
            topic=clean_topic,
            fact=clean_fact,
            explanation="Contributed by a Beyond the Temperature visitor.",
            solution=clean_solution,
        )
        state.climate_facts.append(created_fact)
        state.current_fact = created_fact
        state.facts_viewed = state.facts_viewed + 1

    return fact_page(state)


@route
def submit_feedback(
    state: State, user_name: str, selected_topic: str, pledge_checked: bool
) -> Page:
    """Processes the user's feedback form and updates state."""
    state.current_topic = selected_topic
    state.feedback_message = build_topic_feedback(
        user_name, selected_topic, pledge_checked
    )
    return home(state)


# ---------------------------------------------------------------------------
# Unit Tests (Every deterministic helper and route is tested below)
# ---------------------------------------------------------------------------
# 1. Helper Function Tests
test_facts = create_default_facts()
assert_equal(len(test_facts), 5)
assert_equal(test_facts[0].topic, "Food")

formatted_sample = format_all_facts([
    ClimateFact("Sleep", "Warm nights cut sleep.", "Heat rises.", "Use fans.")
])
assert_equal(
    formatted_sample,
    ["[Sleep] Warm nights cut sleep. — Action: Use fans."],
)

assert_equal(
    build_topic_feedback("Alex", "Food", True),
    "Thank you, Alex! We are glad you enjoyed the Food section! Protecting "
    "crops like coffee and cocoa starts with sustainable agriculture. "
    "Thank you for committing to share a climate fact with a friend!",
)
assert_equal(
    build_topic_feedback("", "Sleep", False),
    "Thank you, Climate Explorer! We are glad you enjoyed the Sleep section! "
    "Cooler cities and green spaces help everyone rest better at night. "
    "Consider sharing one fact you learned today with a friend!",
)
assert_equal(
    build_topic_feedback("Sam", "Insects", True),
    "Thank you, Sam! We are glad you enjoyed the Insects section! Managing "
    "standing water helps keep communities safe from vector-borne illness. "
    "Thank you for committing to share a climate fact with a friend!",
)

assert_equal(
    get_milestone_banner(2),
    "Facts explored so far: 2 (View 5 facts to unlock Climate Expert status!)",
)
assert_equal(
    get_milestone_banner(5),
    "🌟 Wow, you're a climate expert! You've read 5 facts.",
)

# 2. Route Tests
state_for_index = create_initial_state()
assert_equal(index(state_for_index).state.current_topic, "Home")

state_for_home = create_initial_state()
state_for_home.current_topic = "Food"
assert_equal(home(state_for_home).state.current_topic, "Home")

state_for_food = create_initial_state()
assert_equal(food_page(state_for_food).state.current_topic, "Food")

state_for_sleep = create_initial_state()
assert_equal(sleep_page(state_for_sleep).state.current_topic, "Sleep")

state_for_insects = create_initial_state()
assert_equal(insects_page(state_for_insects).state.current_topic, "Insects")

state_for_facts = create_initial_state()
assert_equal(fact_page(state_for_facts).state.current_topic, "Fact Explorer")

state_for_add = create_initial_state()
updated_add_page = add_custom_fact(
    state_for_add,
    "Oceans",
    "Sea levels are rising faster each decade.",
    "Reduce carbon emissions.",
)
assert_equal(len(updated_add_page.state.climate_facts), 6)
assert_equal(updated_add_page.state.facts_viewed, 2)
assert_equal(
    updated_add_page.state.current_fact.fact,
    "Sea levels are rising faster each decade.",
)

state_for_feedback = create_initial_state()
updated_feedback_page = submit_feedback(
    state_for_feedback, "Jordan", "Food", True
)
assert_equal(
    updated_feedback_page.state.feedback_message,
    "Thank you, Jordan! We are glad you enjoyed the Food section! Protecting "
    "crops like coffee and cocoa starts with sustainable agriculture. "
    "Thank you for committing to share a climate fact with a friend!",
)
# Note: another_fact() uses random.choice() and cannot be deterministically
# unit tested, as documented in its docstring above.


# ---------------------------------------------------------------------------
# Launch Server
# ---------------------------------------------------------------------------
start_server(create_initial_state())
