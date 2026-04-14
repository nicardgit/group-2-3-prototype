import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import json
import base64


# --- PAGE CONFIG ---
st.set_page_config(page_title="Group 2.3 - Data Centers and Water", layout="wide")

# --- GLOBAL FONT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

    * {
        font-family: 'Helvetica', serif !important;
    }

    h1 {
        font-size: 2.8rem !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
    }

    h2, h3 {
        font-weight: 600 !important;
    }

    p {
        font-size: 1.1rem !important;
        line-height: 1.1 !important;
        text-indent: 2rem !important;
    }

    /* Remove Streamlit padding */
    .stApp {
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
        max-width: 800px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin: 0 auto !important;
    }

    /* Hide Streamlit header bar */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    .viz-fullwidth {
        width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        margin-right: calc(-50vw + 50%) !important;
        position: relative;
        overflow: hidden;
    }

    .viz-fullwidth > iframe {
        width: 100vw !important;
        display: block;
    }

    </style>
""", unsafe_allow_html=True)

# -- ADDING AN IMAGE --

def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

cooling_img = get_base64_image("cooling_floor.jpg")
yellow_hallway_img = get_base64_image("yellow_hallway.jpg")
water_cooling_img = get_base64_image("water_cooling.jpg")
hero_img = get_base64_image("ups_room.jpg")
predict_map = get_base64_image("US.data.center.jpg")

# -- ADDING AN HTML --

def get_html_content(html_file, height=600):
    with open(html_file, "r") as f:
        content = f.read()
    encoded = base64.b64encode(content.encode()).decode()
    return f"""
        <div style="
            position: relative;
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            margin-right: calc(-50vw + 50%);
            height: {height}px;
            overflow: hidden;
        ">
            <iframe
                src='data:text/html;base64,{encoded}'
                style='
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border: none;
                '
                scrolling="no">
            </iframe>
        </div>
    """

plot_html = get_html_content("plot_2_interactive.html")
water_stress_map_html = get_html_content("interactive_map_10.html")
data_center_predict = get_html_content("datacenter_water_consumption.html")

# -- ADDING A VIDEO --

def get_base64_video(video_file):
    with open(video_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

video_base64 = get_base64_video("hey_chat.mp4")

# -- ADDING AN AUDIO --

def get_base64_audio(audio_file):
    with open(audio_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

ups_room = get_base64_audio("ups_room.mp3")

# -- CHAT EXCHANGE --

def chat_exchange(pairs, height=600):
    bubbles_html = ""

    for i, (question, answer) in enumerate(pairs):
        q = question or ""
        a = answer or ""

        # Special divider type
        if q == "__DIVIDER__":
            bubbles_html += f"""
            <div class="chat-wrapper" id="pair-{i}" style="opacity:0; transform: translateY(30px); transition: opacity 0.5s ease, transform 0.5s ease;">
                <hr style="border: none; border-top: 1px solid #ddd; margin: 2rem 0;"/>
            </div>
            """
            continue

        question_html = f"""
        <div class="typing-container question-container">
            <div class="chat-bubble question-bubble">
                <span id="q-text-{i}"></span>
            </div>
        </div>
        """ if q else ""

        is_viz = a.strip().startswith('<iframe')
        bubble_class = "viz-bubble" if is_viz else "response-bubble"

        bubbles_html += f"""
            <div class="chat-wrapper" id="pair-{i}" style="opacity:0; transform: translateY(30px); transition: opacity 0.5s ease, transform 0.5s ease;">
            {question_html}
             <div class="typing-container response-container">
        <div class="chat-bubble {bubble_class}">
            <span id="a-text-{i}"></span>
                </div>
            </div>
        </div>
        """

    questions_js = json.dumps([q or "" for q, a in pairs])
    answers_js = json.dumps([a or "" for q, a in pairs])

    components.html(f"""
    <style>
    .chat-wrapper {{
        margin-bottom: 1.5rem;
    }}

    .typing-container {{
        display: flex;
        margin: 0.4rem 0;
    }}

    .question-container {{
        justify-content: flex-end;
    }}

    .response-container {{
        justify-content: flex-start;
    }}

    .chat-bubble {{
        padding: 0.8rem 1.2rem;
        border-radius: 18px;
        font-family: sans-serif;
        font-size: 1.125rem;
        line-height: 1.6;
        max-width: 80%;
    }}

    .question-bubble {{
        background: #08306B;
        color: white;
    }}

    .response-bubble {{
        background: #f1f1f1;
        color: black;
    }}

    .viz-bubble {{
        background: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }}
    </style>

    {bubbles_html}

    <script>
    const questions = {questions_js};
    const answers = {answers_js};
    let currentPair = 0;
    let isTyping = false;

    function typeText(el, text, speed, callback) {{
        if (text.trim().startsWith('<img') || text.trim().startsWith('<iframe')) {{
            el.innerHTML = text;
            if (callback) callback();
            return;
        }}

        let i = 0;

        function typing() {{
            if (i < text.length) {{
                el.innerHTML = text.slice(0, i + 1);
                i++;
                setTimeout(typing, speed);
            }} else if (callback) {{
                callback();
            }}
        }}

        typing();
    }}

    function typePair(i) {{
        if (isTyping) return;
        isTyping = true;

        const wrapper = document.getElementById("pair-" + i);
        wrapper.style.opacity = "1";
        wrapper.style.transform = "translateY(0)";

        // Handle divider — show instantly and move on
        if (questions[i] === "__DIVIDER__") {{
            isTyping = false;
            currentPair++;
            observeNext();
            return;
        }}

        const qEl = document.getElementById("q-text-" + i);
        const aEl = document.getElementById("a-text-" + i);

        if (questions[i]) {{
            typeText(qEl, questions[i], 25, () => {{
                setTimeout(() => {{
                    typeText(aEl, answers[i], 15, () => {{
                        isTyping = false;
                        currentPair++;
                        observeNext();
                    }});
                }}, 400);
            }});
        }} else {{
            typeText(aEl, answers[i], 15, () => {{
                isTyping = false;
                currentPair++;
                observeNext();
            }});
        }}
    }}

    function observeNext() {{
        if (currentPair >= questions.length) return;

        const nextWrapper = document.getElementById("pair-" + currentPair);
        if (!nextWrapper) return;

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    observer.unobserve(entry.target);
                    typePair(currentPair);
                }}
            }});
        }}, {{ threshold: 0.3 }});

        observer.observe(nextWrapper);
    }}

    observeNext();

    </script>
    """, height=height, scrolling=True)


# --- ABOVEFOLD ---

st.markdown(f"""
    <style>
    #video-container {{
        position: relative;
        width: 100vw !important;
        height: 100vh;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-left: calc(-50vw + 50%) !important;
    }}

    #bg-video {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        min-width: 100%;
        min-height: 100%;
        z-index: 0;
        object-fit: cover;
    }}

    #scroll-indicator {{
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 2;
        color: white;
        font-size: 0.85rem;
        font-family: Helvetica, sans-serif;
        text-align: center;
        animation: bounce 2s infinite;
    }}

    @keyframes bounce {{
        0%, 100% {{ transform: translateX(-50%) translateY(0); }}
        50% {{ transform: translateX(-50%) translateY(-10px); }}
    }}
    </style>

    <div id="video-container">
        <video id="bg-video" autoplay muted loop playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        <div id="scroll-indicator">
            ↓ scroll to read
        </div>
    </div>

""", unsafe_allow_html=True)

# -- TITLE AND AUTHORS --
st.markdown(f"""
    <style>
    #hero-container {{
        position: relative;
        width: 100vw !important;
        height: 100vh;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-left: calc(-50vw + 50%) !important;
        margin-right: calc(-50vw + 50%) !important;
    }}

    #hero-bg {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 120%;
        background-image: url('data:image/jpeg;base64,{hero_img}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        z-index: 0;
        transform: scale(1.1);   # <-- add this line
        will-change: transform;  # <-- and this for smoother animation
    }}

    #hero-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1;
    }}

    #hero-content {{
        position: relative;
        z-index: 2;
        text-align: center;
        padding: 2rem;
        max-width: 800px;
        opacity: 1;
        transform: translateY(0);
    }}

    #hero-content h1 {{
        font-family: 'Merriweather', serif;
        font-size: 3.5rem;
        color: white;
        line-height: 1.3;
        margin-bottom: 1rem;
    }}

    #hero-content h4 {{
        font-family: 'Helvetica', sans-serif;
        font-size: 1.2rem;
        color: #dddddd;
        font-weight: 400;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }}

    #hero-content p {{
        font-family: 'Helvetica', sans-serif;
        font-size: 0.9rem;
        color: #aaaaaa;
        text-indent: 0 !important;
    }}

    #scroll-indicator {{
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 2;
        color: white;
        font-size: 0.85rem;
        font-family: Helvetica, sans-serif;
        text-align: center;
        animation: bounce 2s infinite;
    }}

    @keyframes bounce {{
        0%, 100% {{ transform: translateX(-50%) translateY(0); }}
        50% {{ transform: translateX(-50%) translateY(-10px); }}
    }}
    </style>

    <div id="hero-container">
        <div id="hero-bg"></div>
        <div id="hero-overlay"></div>
        <div id="hero-content">
            <h1>Can data centers be sustainable?</h1>
            <h4>Many countries are scrambling to establish more data centers that can handle higher workloads to meet the heightened demand for generative AI, raising concerns over the volume of water needed to cool and operate these infrastructures.</h4>
            <p>by Nica Rhiana Hanopol, Vadim Martschenko, and Lara Zofio</p>
        </div>
    </div>
""", unsafe_allow_html=True)

## -- SCROLL EFFECTS --
components.html("""
<script>
  function applyScrollEffects() {
    const scrollY = window.parent.scrollY;
    const heroBg = window.parent.document.getElementById('hero-bg');
    const heroContent = window.parent.document.getElementById('hero-content');

    if (!heroBg || !heroContent) return;

    const heroH = window.parent.document.getElementById('hero-container').offsetHeight;
    const progress = Math.min(scrollY / heroH, 1);

    // Parallax background
    heroBg.style.transform = `scale(1.1) translateY(${scrollY * 0.3}px)`;

    // Fade + float text out
    heroContent.style.opacity = Math.max(1 - progress * 1.8, 0);
    heroContent.style.transform = `translateY(${-scrollY * 0.2}px)`;
  }

  window.parent.addEventListener('scroll', applyScrollEffects);
</script>
""", height=0)

st.divider()

# --- LEDE ---

st.markdown("<p>As a European, you won't consume as much water in your entire lifetime as a data center does in a single year. Yes, the kind of data center needed to run the ubiquitous digital technology we all use today, including AI.</p>", unsafe_allow_html=True)

st.markdown("<p>It would take one person about 485 years to use up all that water. According to the <a href='https://www.weforum.org/stories/2024/11/circular-water-solutions-sustainable-data-centres/' target='_blank'>World Economic Forum</a>, a single 1-megawatt data center can consume up to 25.5 million liters of water annually for cooling alone. That's equivalent to around 10 Olympic-sized swimming pools every year.</p>", unsafe_allow_html=True)

st.markdown("<p>And that's just for cooling. Factor in the water used in electricity generation, and that figure triples.</p>", unsafe_allow_html=True)

st.markdown("<p>Meanwhile, according to the United Nations (UN), the world is already living in a state of <a href='https://news.un.org/en/story/2026/01/1166800' target='_blank'>“water bankruptcy”</a> – withdrawing and polluting water more than it can replenish. About three-quarters of the population live in countries considered water-insecure or critically water-insecure, a January <a href='https://unu.edu/inweh/collection/global-water-bankruptcy' target='_blank'>report</a> by the UN University Institute of Water, Environment, and Health stated.</p>", unsafe_allow_html=True)

# -- INSERT WATER STRESS MAP --
st.markdown("<div class='viz-fullwidth'>", unsafe_allow_html=True)
with open("interactive_map_10.html", "r") as f:
    html_content = f.read()
components.html(f"""
    <style>
    html, body {{
        margin: 0;
        padding: 0;
        width: 100vw;
        max-width: 100vw;
        overflow-x: hidden;
    }}
    </style>
    {html_content}
""", height=700, scrolling=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:0.7rem; color:#888; text-indent:0; text-align:center;'>Data Sources: UN FAO AquaStat (2022)</p>",
    unsafe_allow_html=True
)

st.markdown("<p>Data centers have emerged as the latest threat to already strained water supplies, increasing in complexity, size, and number to meet the surging demand for generative AI.</p>", unsafe_allow_html=True)

st.markdown("<p>Driven by economic incentives, the protection of industry interests, and, ultimately, national digital sovereignty, the AI bubble is expanding, even where water conditions cannot support it. This calls for sustainable infrastructure, such as using renewable energy that consumes much less water to run a data center.</p>", unsafe_allow_html=True)

# -- INSERT GLOBAL DATA CENTER DISTRIBUTION MAP --
st.markdown("<div class='viz-fullwidth'>", unsafe_allow_html=True)
with open("plot_2_interactive.html", "r") as f:
    html_content = f.read()
components.html(f"""
    <style>
    html, body {{
        margin: 0;
        padding: 0;
        width: 100vw;
        max-width: 100vw;
        overflow-x: hidden;
    }}
    </style>
    {html_content}
""", height=700, scrolling=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:0.7rem; color:#888; text-indent:0; text-align:center;'>Data Sources: UN FAO AquaStat and Our World in Data (2022)</p>",
    unsafe_allow_html=True
)

st.markdown("<p>We don't have to travel too far to find an example: Denmark actively markets itself as a country with “ideal conditions” for data centers, by running on more than 88.4% of renewable energy as of 2024, having average annual temperatures of around 10 degrees Celsius and abundant freshwater supplies that all facilitate cooling of these facilities.</p>", unsafe_allow_html=True)

st.markdown("<p>So we decided to visit one of <a href='https://www.datacentermap.com/denmark/' target='_blank'>82</a> data centers in the country to see how it operates firsthand.</p>", unsafe_allow_html=True)

st.divider()

# --- SUBHEAD 1: INTRO TO KOLO ---

chat_exchange([("What is Denmark doing exactly?",
        "Ten miles into East Jutland, the road opens to a Danish panorama: uniform warehouses and nothing on the streets but the rumble of delivery trucks passing by. Out in the stretch of Skanderborg lies one infrastructure in Denmark's digital backbone: a 740-square-meter data center with roughly 800 kilowatts of energy capacity. The colocation facility, owned by Kolo, formerly Fuzion A/S, rents out racks to at least 80 clients across financial, healthcare, and public sector organizations."),

        ("",
        "Martin Andersen, site manager and a marine engineer, guides us through the data center."),

        ("",
        f"<img src='data:image/jpeg;base64,{yellow_hallway_img}' style='width:100%; border-radius:16px; margin-top:0.6rem;'/>"),

        ("",
         "Everything we do on the internet, however immaterial it may seem, requires physical hardware. Every search query, every streaming service, and every piece of data is housed in data centers, like Kolo's DK1 facility."),

        ("",
        "We enter a grey room full of server boxes and cables."),

        ("",
        f"<img src='data:image/jpeg;base64,{hero_img}' style='width:100%; border-radius:16px; margin-top:0.6rem;'/>"),

         ], height=2300)

## -- INSERT AUDIO -- 
components.html(f"""
<style>
  #audio-bubble {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }}
  #audio-bubble.visible {{
    opacity: 1;
    transform: translateY(0);
  }}
</style>

<div id="audio-bubble" style="display:flex; align-items:center; padding:1rem;
     background:#f1f1f1; border-radius:18px; max-width:500px; font-family:sans-serif;">
  <audio controls style="width:100%;">
    <source src="data:audio/mp3;base64,{ups_room}" type="audio/mp3">
  </audio>
</div>

<script>
  const bubble = document.getElementById('audio-bubble');
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        bubble.classList.add('visible');
        observer.unobserve(bubble);
      }}
    }});
  }}, {{ threshold: 0.4 }});
  observer.observe(bubble);
</script>
""", height=90, scrolling=False)
        
chat_exchange([("",
        "The low temperature in the room matches the cold weather outside. Looking down, we see small fans on the floor, which are producing cool air."),

        ("",
        "Unlike other facilities that use evaporative cooling systems, Andersen says, “We have chosen not to do that. We actually see water as a more scarce resource than power.”"),

        ("",
        "Cooling systems are one of the reasons for the exorbitant water consumption in data centers. Estimates suggest that about a third of their total water footprint comes from on-site cooling, while the rest stems from electricity generation and chip production. This underscores the importance of renewable energy sources, such as wind and solar power, which <a href='https://www.eesi.org/articles/view/data-centers-and-water-consumption#:~:text=POwering%20data%20centers,like%20coal%20and%20natural%20gas' target='_blank'>use much less water</a>."),

        ("",
        "But AI changes the game. With ChatGPT, Gemini, and Copilot as their newest occupants, data centers demand far more computing power, energy, and water than the traditional storage tasks they were built for."),

        ("",
        "According to research from the <a href='https://arxiv.org/pdf/2304.03271' target='_blank'>University of California Riverside</a>, ten simple AI search queries can consume up to 500ml of water."),

        ("",
         "Andersen explains that AI data centers cannot simply use airflow to cool equipment. “You either have to cool it on the chip, on-chip cooling, or with what they call rear door cooling. Instead of having the heat exchanger far away, you put it directly in the back of the rack,” he adds."),

        ("",
        "Bundled up in our coats, we follow him outside into a spring morning so cold and windy that the servers can cool themselves."),

        ("",
        f"<img src='data:image/jpeg;base64,{water_cooling_img}' style='width:100%; border-radius:16px; margin-top:0.6rem;'/>"),

        ("",
        "“We have very low water consumption,” Andersen says, “because of the low temperature.” Between October and April, consumption drops to practically zero. Soon, Kolo also expects to harness waste heat from the data center to connect to the district heating network, which could provide heat to “approximately 1,500 homes.”"),

        ("",
        "As data center operators and public institutions rarely disclose water and electricity consumption, precise comparisons between sustainable and traditional data centers remain difficult. The industry is opaque, and the conflict between demand and climate goals keeps estimations uncertain."),

        ("",
        "Using available data from the US, we see how the country's water consumption in data centers rose from 21.2 billion in 2014 to 66 billion in 2023. Projections range from 1.5 billion liters in an ideal sustainable scenario to exorbitant levels if inefficient systems and fossil-fuel reliance continue."),

# -- INSERT DATACENTER WATER CONSUMPTION CHART --

        ("",
        f"<img src='data:image/jpeg;base64,{predict_map}' style='width:100%; border-radius:16px; margin-top:0.6rem;'/>"),

    ], height=2500)

st.divider()

# --- SUBHEAD 2: DATA CENTERS FOLLOW THE MONEY ---

chat_exchange([("Do water conditions explain where data centers are built?",
        "Although countries such as Denmark argue that they may have the ideal conditions for minimizing the environmental impacts of data centers, an analysis of global data from 2022 found that these factors rarely determine where such facilities are actually built."),

        ("",
         "Compiling data from UN Aquastat and Our World in Data, we explored how water stress and renewable energy share relate to data center counts across countries. If these factors explained the latter, we would expect to see significantly more counts in countries with lower water stress and higher renewable energy."),

        ("",
          "Neither of these factors, however, turned out to be the main driver. Instead,  our model showed that wealth is what matters most. For every doubling of gross domestic product (GDP), nearly 38 additional data centers were built. This is substantial, given that a country like Germany has a GDP more than ten times than that of Denmark."),

        ("",
          "Greenpeace's AI experts Jonathan Niesel and Linda Klapdor pointed out that grid capacity, high internet connectivity, and government incentives largely determine where data centers are located."),

        ("",
         "“The last thing that people look for is water because you can just cool without water,” says Niesel."),

        ("",
        "Only in extreme cases of drought does water begin to matter, like in <a href='https://www.theguardian.com/global-development/2025/may/22/datacentre-drought-chinese-social-media-supercomputers-brazil-latin-america' target='_blank'>Latin America</a>, where data centers are reportedly depleting local water supplies while providing little to no economic benefit to nearby communities."),

        ("",
        "For Greenpeace, the AI boom is also an issue of power struggle. “Maybe some countries don't actually want that [many data centers], but then there's a fear of missing out on this great new technology,” Klapdor says."),

        ("",
         "Hence, there is a risk of widening the gap between Global North and Global South: If the <a href='https://ddrn.dk/16310/#:~:text=Global%20South%20Countries%20are%20more,of%20the%20earth%20than%20before.' target='_blank'>Global South</a> were to build data centers at the same rate as wealthier nations, these countries could experience greater negative climate impacts, especially on their water stress levels."),

         ("__DIVIDER__", ""),

# -- SUBHEAD 3: WHAT NEEDS TO BE DONE? --

        ("What needs to be done?",
        "The question is not whether data centers should exist or not, but rather how they can be governed to be sustainable and fair."),
        
        ("",
         "“You have to make the decision what you need the data centers for. Of course, we don't need another Sora app that is generating videos, but you need data centers in the modern economy,” says Niesel, stressing the need for the “right guardrails.”"),

         ("",
          "The European Union's (EU) <a href='https://energy.ec.europa.eu/topics/energy-efficiency/energy-efficiency-targets-directive-and-rules/energy-efficiency-directive_en#energy-performance-of-data-centres' target='_blank'>Energy Efficiency Directive</a>, introduced in 2023, is a first step. Data centers with a capacity over 500kWh in the EU must publicly report key energy metrics, including aggregates of water consumption. Additionally, if the facility exceeds 1 MW capacity, it is required to run entirely on renewable energy by 2050 and utilize waste heat."),

        ("",
        "With this, the EU aims to lessen its dependence on US tech giants by expanding its data center infrastructure, while maintaining strict sustainability standards."),

        ("",
        "Still, Niesel notes that a fully sustainable data center remains difficult for the industry. And when it comes to AI, Klapdor asks, “To what extent do we need it?”"),

   ], height=2070)

st.caption("end chat", unsafe_allow_html=True)
st.divider()

## -- METHODOLOGY BOX -- ##

st.markdown("<h1>METHODOLOGY</h1>", unsafe_allow_html=True)
st.markdown("<p>Researchers used RStudio to run linear regression models with 20 data from <a href='https://www.fao.org/aquastat/en' target='_blank'>UN AquaStat</a>, <a href='http://google.com/search?q=world+bank+gdp&oq=world+bank+gdp&gs_lcrp=EgZjaHJvbWUqCQgAEEUYOxiABDIJCAAQRRg7GIAEMgcIARAAGIAEMgcIAhAAGIAEMgcIAxAAGIAEMgcIBBAAGIAEMgcIBRAAGIAEMgcIBhAAGIAEMgcIBxAAGIAEMgcICBAAGIAEMgcICRAAGIAE0gEIMjM3MGowajSoAgCwAgA&sourceid=chrome&ie=UTF-8' target='_blank'>World Bank</a>, <a href='https://globaldatalab.org/geos/table/surfacetempyear/' target='_blank'>Global Data Lab</a>, and <a href='https://www.datacentermap.com/' target='_blank'>Data Center Map</a>. Water stress levels (%) and renewable energy share (%) were modeled as independent variables, while the counts of data centers was the dependent variable. GDP (US$) and temperature (in degree Celsius) were introduced as control variables.</p>", unsafe_allow_html=True)

# --- FOOTER ---
st.divider()

st.caption("This article was produced as part of the course Applied Quantitative Research and Journalism Practice at Aarhus University under the Erasmus Mundus Journalism, Media, and Globalization program. The data and code used in this project are available on our GitHub repository.", unsafe_allow_html=True)