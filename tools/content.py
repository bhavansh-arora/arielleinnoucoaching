"""
Copy, links and lists for the Arielle Innou Coaching site.

Everything here comes from arielleinnoucoaching.com. Edit it and run
`python3 tools/build.py` to regenerate the pages (pages already saved from the
visual editor are left alone unless you pass --force).
"""

# Live address: used for canonical URLs, share cards and sitemap.xml.
SITE_URL = "https://arielleinnoucoaching.codebunny.net"
SITE_NAME = "Arielle Innou Coaching"

EMAIL = "arielle@arielleinnoucoaching.com"
LOCATION = "Toronto, Ontario"

# Applications and registration (JotForm forms used on the current site).
APPLY_LIFE = "https://form.jotform.com/251975488693074"
APPLY_CORPORATE = "https://form.jotform.com/251906297424058"  # same form the current site's corporate page embeds
REGISTER_RETREAT = "https://form.jotform.com/251906297424058"
RETREAT_INSTAGRAM = "https://www.instagram.com/bellaestategardens/"

# The inquiry form posts here. Create a free form at formspree.io and paste its ID;
# until then the form runs in demo mode (validates and thanks, sends nothing).
FORMSPREE_ID = "YOUR_FORM_ID"

CTA = "Book your free 30-minute call"

TESTIMONIALS = [
    ("Sophia G.", "I had lost my identity trying to please everyone else. With Arielle’s support, I found my voice and reclaimed my power.", "Life & Relationship Coaching"),
    ("Caroline L.", "Arielle’s coaching gave me the confidence to trust my instincts and make bold decisions. My life has completely changed.", "Life & Relationship Coaching"),
    ("Denise A.", "She didn’t try to ‘fix’ me—she helped me remember who I really am.", "Life & Relationship Coaching"),
]

HOME_STEPS = [
    ("Schedule your complimentary 30-minute call.", "This allows us to determine if our approaches align effectively.", "arielle-garden"),
    ("Create a custom Clarity Plan.", "Designed to break old patterns and set new boundaries.", "meditation"),
    ("Live life on your terms.", "Embrace a future where you confidently navigate life on your own terms, grounded in peace and a strong sense of self.", "women-joy"),
]
LIFE_STEPS = [
    ("Schedule your complimentary 30-minute consultation.", "Let’s see if we’re a good fit.", "arielle-garden"),
    ("The creation of a tailored Clarity Plan.", "Designed to break old patterns and set new boundaries.", "meditation"),
    ("Live life on your terms.", "With confidence, peace, and a strong sense of self.", "women-joy"),
]
CORP_STEPS = [
    ("Schedule your complimentary 30-minute call.", "Let’s see if we’re a good fit.", "arielle-circle"),
    ("Create a custom Clarity Plan.", "Designed to break old patterns and set new boundaries.", "women-joy"),
    ("Live life on your terms.", "With confidence, peace, and a strong sense of self.", "sisterhood"),
]

COST = [
    "Consistently prioritizing the needs of others over your own.",
    "Experiencing depleted energy due to persistent workplace tension.",
    "Navigating life with decisions clouded by anxiety.",
    "Feeling unwarranted guilt for desiring personal fulfillment.",
]
POWER = [
    "Set healthy boundaries with ease and confidence.",
    "Resolve personal and professional conflicts with confidence.",
    "Feel empowered to make choices that serve your true self.",
    "Live unapologetically, knowing exactly who you are and what you want.",
]

BELIEFS = [
    ("You are not broken.", "You may just be emotionally exhausted."),
    ("Conflict is a clue,", "not a failure—internal or external."),
    ("Boundaries aren’t barriers;", "they’re bridges to healthier relationships."),
    ("Growth doesn’t have to be lonely.", "You don’t have to do it all alone."),
    ("There’s no “too late”", "when it comes to rediscovering yourself."),
]

# About: "My story is one of resilience", told in chapters.
STORY = [
    ("Fez, Morocco", "Where it began", "Growing up as part of a minority community in Fez, Morocco, I experienced firsthand the power of identity and the pain of being misunderstood, navigating environments where freedom of expression was limited and daily life presented unique challenges.", "arielle-chapel"),
    ("France", "Boarding school, young", "My early experiences included attending boarding school in France at a young age…", None),
    ("Canada", "A new home", "…and later immigrating to Canada. Together, they instilled in me a resilience and the ability to thrive in diverse settings.", None),
    ("Fashion & real estate", "The entrepreneur", "My professional path has been equally varied, from entrepreneurship in fashion and real estate…", None),
    ("25 years in healthcare", "The corporate leader", "…to over two decades as a corporate leader in the dental industry, where I excelled in management, mentorship, and business development.", "arielle-circle"),
    ("Life coaching", "The calling", "Throughout it all, my true calling has been to empower individuals to find their voice, resolve inner conflicts, and feel truly seen. This passion led me to life coaching.", "arielle-portrait"),
]

WHY = [
    "I’ve led multi-doctor teams through conflict and growth.",
    "I’ve coached women out of burnout and into bold clarity.",
    "I don’t offer quick fixes—I offer sustainable transformation.",
    "I bring real-life experience and deep emotional insight.",
]

LIFE_FEEL = [
    "Seen and validated, often for the first time in years",
    "Heard without judgment",
    "Supported in setting boundaries without guilt",
    "Empowered to make decisions that serve you",
]
LIFE_TOGETHER = [
    "Break old patterns that no longer serve you",
    "Heal relationship wounds—past or present",
    "Reconnect with your passions, values, and voice",
    "Cultivate clarity, confidence, and peace of mind",
]
LIFE_INCLUDED = [
    ("video", "Private 1:1 sessions", "Via Zoom or in person—whichever feels right for you."),
    ("compass", "Customized Clarity Plans", "Built around your goals and challenges."),
    ("hand", "Ongoing support", "To help you stay accountable, grow, and shift."),
    ("leaf", "Tools & techniques", "For grounding, self-reflection, and emotional strength."),
]
LIFE_YES = [
    "Set healthy boundaries—without guilt or overexplaining",
    "Leave toxic dynamics—or shift how you show up in them",
    "Reclaim your time, energy, and emotional bandwidth",
    "Feel peace in your relationships and purpose in your life",
    "Walk through life with clarity, confidence, and self-respect",
]
LIFE_NO = [
    "You’ll keep feeling like you’re living someone else’s life.",
    "You’ll stay in relationships that drain you.",
    "You’ll keep putting yourself last—and feeling empty when no one notices.",
]
ROLES = ["Mother", "Wife", "Daughter", "Caregiver", "Boss"]

CORP_RESULTS = [
    "Grew a dental practice’s team by 300%, while maintaining a strong, collaborative culture",
    "Developed onboarding programs that improved retention and morale",
    "Mentored staff into leadership roles—many now serve as managers",
    "Launched internal events and communication structures that brought teams together",
    "Transformed workplaces from reactive to proactive, chaotic to clear",
]
CORP_PROGRAMS = [
    ("Team Coaching & Group Dynamics", "For teams struggling with communication breakdowns, role confusion, or low morale.",
     ["Group sessions focused on team challenges", "Interactive exercises, group coaching, and peer learning", "Tailored content based on assessments and organizational goals"], "women-together"),
    ("Staff Wellness & Culture Transformation", "For companies ready to proactively support employee wellbeing and engagement.",
     ["Emotional wellness check-ins", "Burnout prevention strategies", "Support around inclusion, self-esteem, and cultural differences"], "meditation"),
]
CORP_ROI = [
    ("door", "Reduced turnover & absenteeism", "Employees don’t leave jobs—they leave unhealthy environments. Let’s fix that."),
    ("spark", "Increased productivity", "When people feel safe, respected, and empowered, they show up and perform."),
    ("heart", "Higher morale & engagement", "A healthy workplace isn’t just more efficient—it’s more human. That means better customer service, stronger client relationships, and a reputation people trust."),
]

RETREAT_INCLUDED = [
    ("hand", "A dedicated, supportive team", "Guests feel truly nurtured by a dedicated and supportive team."),
    ("bowl", "Healthy, delicious meals", "Thoughtfully prepared, healthy and delicious, with diverse options."),
    ("lotus", "Yoga & meditation", "Restorative activities to breathe, ground and reset."),
    ("leaf", "Nature immersion", "Lush gardens and the inspiring presence of the natural world."),
    ("chat", "Individualized coaching", "Individualized coaching sessions with Arielle."),
    ("compass", "Insightful workshops", "Activities designed to support personal growth and well-being."),
]
RETREAT_GALLERY = [  # ordered so the 3-column grid packs with no gaps
    ("retreat-gardens", "The formal gardens at Bella Estate Gardens from above"),
    ("retreat-statue", "A garden statue in front of the white chapel"),
    ("arielle-garden", "Arielle hosting a garden luncheon at the estate"),
    ("retreat-chapel", "Inside the estate chapel, with white flowers along the aisle"),
    ("retreat-firepit", "Colourful Muskoka chairs around the fire pit, with the chapel beyond"),
    ("retreat-path", "A tree-lined path in autumn colour"),
    ("arielle-estate", "Arielle walking on the estate lawn"),
    ("retreat-pavilion", "A dinner table set under the garden pavilion"),
    ("retreat-poolside", "Guests by the pool on a summer afternoon"),
    ("arielle-celebration", "Arielle with a guest at an evening celebration"),
    ("retreat-pool", "The pool terrace surrounded by greenery"),
    ("arielle-circle", "Arielle with friends at an evening gathering"),
]

FAQS = [
    ("How does the free 30-minute call work?", "It’s a complimentary, no-pressure conversation. We talk about where you are, where you want to go, and whether our approaches align. If we’re a good fit, we’ll map out next steps together."),
    ("Do you coach online or in person?", "Both. Private 1:1 sessions run via Zoom or in person in Toronto, so you can choose what feels right for you."),
    ("Who do you work with?", "Women in midlife and beyond (often 50+) who want to reclaim their identity, rewrite old stories and build boundaries that protect their peace—and leaders and teams, especially in dental offices, healthcare and small-to-mid-size businesses, who want a healthier, more productive workplace."),
    ("What is a Clarity Plan?", "A custom plan we create together after our first conversation. It’s designed to break old patterns and set new boundaries, based on your goals and challenges."),
    ("Where are the retreats held?", "In the Ontario countryside at Bella Estate Gardens: a beautiful sanctuary of lush gardens, nestled in tranquility away from the busy city."),
]
