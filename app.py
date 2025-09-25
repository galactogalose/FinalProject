import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List
import uuid
import json
import textwrap
import time
from datetime import datetime

# -------------------------
# Enhanced Story Agent
# -------------------------
@dataclass
class StoryNode:
    id: str
    text: str
    choices: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    image_prompt: str = ""  # For AI image generation
    mood: str = "neutral"  # emotional tone

class EnhancedStoryAgent:
    def __init__(self, story_tree: Optional[Dict[str, Any]] = None):
        self.story_nodes: Dict[str, StoryNode] = {}
        self.root_id: Optional[str] = None
        self.achievements: Dict[str, bool] = {}
        if story_tree:
            self.load_tree(story_tree)

    def load_tree(self, tree: Dict[str, Any]):
        self.story_nodes = {}
        for nid, node in tree.items():
            node_obj = StoryNode(
                id=str(nid),
                text=node.get("text", ""),
                choices=node.get("choices", {}),
                metadata=node.get("metadata", {}),
                image_prompt=node.get("image_prompt", ""),
                mood=node.get("mood", "neutral")
            )
            self.story_nodes[str(nid)] = node_obj
        self.root_id = "start" if "start" in tree else next(iter(self.story_nodes)) if self.story_nodes else None

    def get_node(self, node_id: str) -> StoryNode:
        return self.story_nodes[node_id]

    def get_root(self) -> StoryNode:
        if self.root_id is None:
            raise RuntimeError("No root node set in story tree.")
        return self.get_node(self.root_id)

    def add_node(self, text: str, choices: Optional[Dict[str, str]] = None, 
                 image_prompt: str = "", mood: str = "neutral") -> str:
        nid = str(uuid.uuid4())
        self.story_nodes[nid] = StoryNode(id=nid, text=text, choices=choices or {}, 
                                        image_prompt=image_prompt, mood=mood)
        return nid

    def link_choice(self, from_id: str, choice_text: str, to_id: str):
        self.story_nodes[from_id].choices[choice_text] = to_id

    def export_tree(self) -> Dict[str, Any]:
        out = {}
        for nid, node in self.story_nodes.items():
            out[nid] = {
                "text": node.text, 
                "choices": node.choices, 
                "metadata": node.metadata,
                "image_prompt": node.image_prompt,
                "mood": node.mood
            }
        return out

# -------------------------
# Enhanced Sample Story Tree
# -------------------------
def enhanced_sample_story_tree():
    return {
        "start": {
            "text": textwrap.dedent("""
            🌅 **The Awakening**
            
            You awaken beneath a sky painted with violet clouds, the air crisp with unknown magic. 
            At your feet lies a faded map adorned with glowing runes, and before you, two paths diverge:
            
            • A narrow, mysterious trail that disappears into the whispering darkness of an ancient forest
            • A sunlit cobbled road leading to a distant village where chimney smoke dances in the breeze
            """),
            "choices": {
                "🌲 Take the forest trail - embrace the unknown": "forest_entrance",
                "🏡 Walk to the village - seek civilization": "village_gate"
            },
            "image_prompt": "fantasy landscape with violet clouds, ancient map, two diverging paths in magical forest",
            "mood": "mysterious"
        },
        "forest_entrance": {
            "text": textwrap.dedent("""
            🌲 **The Whispering Woods**
            
            The forest envelops you in a cathedral of ancient trees. Silence hangs heavy, broken only by 
            distant whispers that seem to call your name. A soft, ethereal light pulses between the gnarled 
            oaks, while a massive hollow tree trunk gapes like a doorway to forgotten realms.
            """),
            "choices": {
                "✨ Follow the mysterious light - curiosity calls": "mystic_clearing",
                "🚪 Enter the hollow trunk - brave the darkness": "hollow_trunk",
                "🔙 Return to the crossroads - reconsider your path": "start"
            },
            "image_prompt": "enchanted forest with glowing lights, ancient trees, mysterious hollow trunk",
            "mood": "magical"
        },
        "village_gate": {
            "text": textwrap.dedent("""
            🏡 **Ravenwood Village Gates**
            
            The village gates open to reveal a charming settlement bustling with life. A merchant with 
            twinkling eyes offers you a strange amulet that hums with latent power. Nearby, children 
            pause their game to point curiously at your glowing map.
            """),
            "choices": {
                "💎 Buy the mysterious amulet - invest in magic": "amulet_shop",
                "🧠 Politely refuse and ask about the map - seek knowledge": "old_scholar",
                "🔙 Return to the crossroads": "start"
            },
            "image_prompt": "fantasy village gate with merchant, children playing, magical amulet",
            "mood": "hopeful"
        },
        "mystic_clearing": {
            "text": textwrap.dedent("""
            🦌 **The Stag's Clearing**
            
            You emerge into a sun-dappled clearing where an ancient stag with antlers like crystalline 
            branches awaits. Its eyes hold ancient wisdom as it offers a riddle that echoes in your mind:
            
            *'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'*
            """),
            "choices": {
                "🎯 Answer 'an echo' - trust your intuition": "riddle_success",
                "🙏 Withdraw respectfully - some mysteries are not meant to be solved": "forest_exit"
            },
            "image_prompt": "magical clearing with ancient crystalline stag, sunbeams through trees",
            "mood": "wise"
        },
        "hollow_trunk": {
            "text": textwrap.dedent("""
            🔑 **Chamber of Whispers**
            
            Inside the hollow trunk, you find a hidden chamber illuminated by glowing runes that pulse 
            with ancient magic. An iron key rests on a moss-covered stone altar, humming with potential energy.
            """),
            "choices": {
                "🗝️ Take the iron key - embrace your destiny": "key_taken",
                "🚶 Leave it and go back - some power is too great": "forest_entrance"
            },
            "image_prompt": "hidden chamber inside tree trunk with glowing runes, ancient key on altar",
            "mood": "mysterious"
        },
        "amulet_shop": {
            "text": textwrap.dedent("""
            💎 **Visions of the Amulet**
            
            The amulet hums warmly in your palm, and suddenly you're swept into a vision: a lone lighthouse 
            stands against storm-tossed cliffs, its beam cutting through torrential rain like a blade of hope.
            """),
            "choices": {
                "🌊 Follow the vision to the lighthouse - heed the call": "lighthouse_path",
                "🔄 Discard the amulet - reject the vision": "village_gate"
            },
            "image_prompt": "magical amulet showing vision of lighthouse on stormy cliff",
            "mood": "visionary"
        },
        "old_scholar": {
            "text": textwrap.dedent("""
            📚 **The Scholar's Discovery**
            
            An old scholar with spectacles perched on his nose examines your map with trembling hands. 
            'These markings...' he whispers, 'they point to the Library of Whispers - a place thought 
            to be myth, hidden beneath the rolling seas!'
            """),
            "choices": {
                "🌊 Seek the hidden library - pursue knowledge": "undersea_library",
                "🏪 Ignore and explore the village - enjoy the present": "village_market"
            },
            "image_prompt": "old scholar in study examining ancient map with magnifying glass",
            "mood": "discovery"
        },
        "riddle_success": {
            "text": textwrap.dedent("""
            ✅ **The Stag's Blessing**
            
            'An echo!' you declare. The stag bows its magnificent head, and a shimmering ward of protection 
            settles around you like an invisible cloak. 'You have proven worthy,' it whispers into your mind.
            """),
            "choices": {
                "🌳 Continue deeper into the forest - embrace the journey": "forest_depths",
                "🗺️ Return to the map - reconsider your options": "start"
            },
            "image_prompt": "magical stag bestowing protective ward on adventurer in forest",
            "mood": "triumphant"
        },
        "forest_exit": {
            "text": textwrap.dedent("""
            ☀️ **Emerging Renewed**
            
            You step back into the sunlight, carrying the forest's profound silence within you. 
            Sometimes wisdom lies in knowing which mysteries to leave untouched.
            """),
            "choices": {"Return to the crossroads": "start"},
            "image_prompt": "person emerging from dark forest into sunlight, looking back thoughtfully",
            "mood": "peaceful"
        },
        # Enhanced ending nodes with more detail
        "key_taken": {
            "text": textwrap.dedent("""
            🧭 **Ending: The Heart's Compass**
            
            Days later, you find a small chest hidden behind a waterfall. The iron key fits perfectly. 
            Inside, a compass glows with inner light, its needle pointing not north, but toward 
            where your heart truly wishes to go. Your greatest adventure is just beginning...
            
            *Achievement Unlocked: True North of the Heart* 🏆
            """),
            "choices": {},
            "image_prompt": "ancient compass glowing with magical light, pointing toward destiny",
            "mood": "fulfilling"
        },
        "lighthouse_path": {
            "text": textwrap.dedent("""
            🌊 **Ending: Guardian of the Storm**
            
            Following the vision, you reach the storm-lashed cliffs. The lighthouse keeper, an old woman 
            with sea-foam eyes, greets you. 'I've been waiting,' she says, offering you the lantern. 
            You become the new guardian, watching over lost souls at sea for generations to come.
            
            *Achievement Unlocked: Keeper of the Light* 🏆
            """),
            "choices": {},
            "image_prompt": "ancient lighthouse on stormy cliff, keeper holding lantern against the gale",
            "mood": "epic"
        },
        "undersea_library": {
            "text": textwrap.dedent("""
            📖 **Ending: Keeper of Stories**
            
            The map leads you to a hidden cove. At low tide, a crystal door appears. Inside, the Library 
            of Whispers stretches into infinity, each book containing stories never told. You become 
            its guardian, preserving tales that would otherwise be lost to time.
            
            *Achievement Unlocked: Librarian of Lost Tales* 🏆
            """),
            "choices": {},
            "image_prompt": "undersea crystal library with floating books and ancient knowledge",
            "mood": "wonderous"
        },
        "village_market": {
            "text": textwrap.dedent("""
            🛍️ **Ending: Simple Joys**
            
            You trade the map for rare spices and a warm meal at the village inn. As night falls, 
            you realize that sometimes the greatest adventures are found not in ancient magic, 
            but in connection, good food, and stories shared around a fire.
            
            *Achievement Unlocked: Master of the Present Moment* 🏆
            """),
            "choices": {},
            "image_prompt": "bustling fantasy market with spices, food, and happy villagers",
            "mood": "content"
        },
        "forest_depths": {
            "text": textwrap.dedent("""
            🏛️ **Ending: Discoverer of Ruins**
            
            Deep in the forest, you find overgrown ruins humming with ancient power. Placing the stag's 
            ward on a stone altar, hidden chambers unlock revealing manuscripts that rewrite history. 
            Your discoveries change how the world understands its own past.
            
            *Achievement Unlocked: Archaeologist of the Arcane* 🏆
            """),
            "choices": {},
            "image_prompt": "ancient overgrown ruins with magical artifacts and ancient manuscripts",
            "mood": "discovery"
        },
    }

# -------------------------
# Enhanced Streamlit UI
# -------------------------
st.set_page_config(
    page_title="📖 Narrative Nexus - Enhanced Storyteller", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .story-text {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0px;
    }
    .ending-node {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0px;
    }
    .choice-btn {
        margin: 5px 0px;
        width: 100%;
    }
    .achievement-badge {
        background-color: #FFD700;
        color: black;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Main title with better formatting
st.title("📖 Narrative Nexus — Enhanced Storyteller")
st.markdown("### Craft Your Adventure, Shape Your Destiny ✨")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎮 Story Controls")
    
    # Initialize session state
    if "agent" not in st.session_state:
        agent = EnhancedStoryAgent(enhanced_sample_story_tree())
        st.session_state.agent = agent
        st.session_state.progress = [agent.root_id]
        st.session_state.current_node = agent.root_id
        st.session_state.story_text = [agent.get_node(agent.root_id).text]
        st.session_state.achievements = set()
        st.session_state.start_time = datetime.now()
        st.session_state.choices_made = 0

    agent = st.session_state.agent

    # Control buttons
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        if st.button("🔄 Restart Story", use_container_width=True):
            st.session_state.progress = [agent.root_id]
            st.session_state.current_node = agent.root_id
            st.session_state.story_text = [agent.get_node(agent.root_id).text]
            st.session_state.achievements = set()
            st.session_state.choices_made = 0
            st.session_state.start_time = datetime.now()
            st.success("✨ Story restarted!")
            st.rerun()

    with col1_2:
        if st.button("⏪ Undo Last Choice", use_container_width=True):
            if len(st.session_state.progress) > 1:
                st.session_state.progress.pop()
                st.session_state.current_node = st.session_state.progress[-1]
                st.session_state.story_text = st.session_state.story_text[:-1]
                st.session_state.choices_made -= 1
                st.info("↩️ Undid last choice.")
                st.rerun()
            else:
                st.warning("📝 Nothing to undo — you're at the beginning.")

    # Story statistics
    st.markdown("---")
    st.subheader("📊 Story Statistics")
    time_elapsed = datetime.now() - st.session_state.start_time
    st.write(f"**Choices made:** {st.session_state.choices_made}")
    st.write(f"**Time playing:** {time_elapsed.seconds // 60} minutes")
    st.write(f"**Achievements:** {len(st.session_state.achievements)}/5")
    
    if st.session_state.achievements:
        st.markdown("**Your Achievements:**")
        for achievement in st.session_state.achievements:
            st.markdown(f'<span class="achievement-badge">{achievement}</span>', unsafe_allow_html=True)

    # Advanced editing features
    st.markdown("---")
    st.subheader("🛠️ Story Crafting Tools")
    
    with st.expander("✍️ Extend Story Tree", expanded=False):
        st.info("Add new branches to your adventure")
        
        new_text = st.text_area("New scene description:", height=100, 
                               placeholder="Describe what happens in this new scene...")
        image_prompt = st.text_input("AI image prompt (optional):", 
                                    placeholder="Visual description for this scene")
        mood = st.selectbox("Scene mood:", ["neutral", "mysterious", "magical", "hopeful", "wise", "discovery", "epic"])
        
        col_new = st.columns(2)
        with col_new[0]:
            if st.button("Create New Scene", use_container_width=True):
                if new_text.strip():
                    nid = agent.add_node(new_text.strip(), choices={}, 
                                       image_prompt=image_prompt, mood=mood)
                    # Auto-generate a choice label from the first few words
                    label = "Continue to: " + new_text.strip()[:30] + "..."
                    agent.link_choice(st.session_state.current_node, label, nid)
                    st.success(f"🎭 New scene created! It will appear as a choice.")
                else:
                    st.warning("Please write some text for the new scene.")

        with col_new[1]:
            if st.button("Add Branching Choice", use_container_width=True):
                if new_text.strip():
                    nid1 = agent.add_node("You come to a crossroads...", choices={})
                    nid2 = agent.add_node(new_text.strip(), choices={}, image_prompt=image_prompt, mood=mood)
                    
                    agent.link_choice(st.session_state.current_node, "Face a new challenge", nid1)
                    agent.link_choice(nid1, "Take the left path", nid2)
                    agent.link_choice(nid1, "Take the right path", agent.root_id)
                    
                    st.success("🔄 Added branching storyline!")

    with st.expander("💾 Save/Load Story", expanded=False):
        st.download_button("📥 Export Story Tree (JSON)", 
                          json.dumps(agent.export_tree(), indent=2), 
                          file_name=f"story_tree_{datetime.now().strftime('%Y%m%d_%H%M')}.json", 
                          mime="application/json")
        
        uploaded = st.file_uploader("📤 Import Story Tree", type=["json"])
        if uploaded:
            try:
                data = json.loads(uploaded.read())
                agent.load_tree(data)
                st.session_state.progress = [agent.root_id]
                st.session_state.current_node = agent.root_id
                st.session_state.story_text = [agent.get_node(agent.root_id).text]
                st.session_state.achievements = set()
                st.success("📚 Story tree imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to import: {e}")

    # Export story text
    st.markdown("---")
    st.subheader("📖 Export Your Story")
    compiled_story = "\n\n".join([f"Chapter {i+1}:\n{text}" for i, text in enumerate(st.session_state.story_text)])
    
    st.download_button("💾 Download Story as Text", compiled_story, 
                      file_name=f"my_adventure_{datetime.now().strftime('%Y%m%d')}.txt", 
                      mime="text/plain")

with col2:
    # Story display area
    st.header("📖 Your Adventure Unfolds...")
    
    # Progress bar
    if len(st.session_state.progress) > 1:
        progress = min(len(st.session_state.progress) / 10, 1.0)
        st.progress(progress)
        st.caption(f"Story progress: {int(progress * 100)}%")

    # Display story text with mood-based styling
    current_node = agent.get_node(st.session_state.current_node)
    
    # Mood-based styling
    mood_colors = {
        "mysterious": "#6A0DAD",
        "magical": "#FF6B6B", 
        "hopeful": "#4ECDC4",
        "wise": "#FFD166",
        "discovery": "#06D6A0",
        "epic": "#118AB2",
        "peaceful": "#83C5BE",
        "visionary": "#9D4EDD",
        "fulfilling": "#F72585",
        "content": "#43AA8B",
        "triumphant": "#F48C06",
        "wonderous": "#7209B7"
    }
    
    border_color = mood_colors.get(current_node.mood, "#4CAF50")
    
    if not current_node.choices:  # Ending node
        st.markdown(f'<div class="ending-node">', unsafe_allow_html=True)
        st.markdown("### 🏁 Story Conclusion")
        st.markdown(current_node.text)
        
        # Check for achievements in ending text
        if "Achievement Unlocked:" in current_node.text:
            achievement = current_node.text.split("Achievement Unlocked:")[1].split("🏆")[0].strip()
            if achievement not in st.session_state.achievements:
                st.session_state.achievements.add(achievement)
                st.balloons()
                st.success(f"🎉 Achievement Unlocked: {achievement}!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("🎊 You've reached an ending! Restart to explore different paths.")
        
    else:
        # Regular story node
        st.markdown(f'<div class="story-text" style="border-left-color: {border_color}">', unsafe_allow_html=True)
        st.markdown(current_node.text)
        
        # Show image prompt as inspiration
        if current_node.image_prompt:
            with st.expander("🎨 Scene Visualization Idea"):
                st.caption("Prompt for AI image generation:")
                st.code(current_node.image_prompt)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Choices section
    if current_node.choices:
        st.markdown("---")
        st.subheader("🤔 What will you do?")
        
        choices_list = list(current_node.choices.items())
        
        # Display choices in columns for better layout
        if len(choices_list) <= 2:
            cols = st.columns(len(choices_list))
        else:
            cols = st.columns(2)  # Maximum 2 columns
        
        for i, (choice_text, child_id) in enumerate(choices_list):
            col_idx = i % 2 if len(choices_list) > 2 else i
            with cols[col_idx]:
                if st.button(choice_text, key=f"choice_{i}", use_container_width=True):
                    # Add typing effect simulation
                    with st.spinner("Continuing your story..."):
                        time.sleep(0.5)  # Small delay for immersion
                    
                    st.session_state.progress.append(child_id)
                    st.session_state.current_node = child_id
                    st.session_state.story_text.append(agent.get_node(child_id).text)
                    st.session_state.choices_made += 1
                    st.rerun()

    # Story path visualization
    if len(st.session_state.progress) > 1:
        st.markdown("---")
        with st.expander("🗺️ Your Journey Path"):
            path_display = " → ".join([f"Step {i+1}" for i in range(len(st.session_state.progress))])
            st.caption(path_display)
            st.progress(len(st.session_state.progress) / max(10, len(st.session_state.progress)))

# -------------------------
# Enhanced Sidebar
# -------------------------
st.sidebar.title("🌟 Enhanced Features")
st.sidebar.markdown("""
### New Improvements:
- **Rich Storytelling**: Enhanced descriptions and emotional depth
- **Visual Atmosphere**: Mood-based styling and image prompts
- **Achievement System**: Unlock badges for different endings
- **Story Statistics**: Track your progress and choices
- **Branching Tools**: Easily extend and modify the story
- **Professional UI**: Better layouts and responsive design

### Tips for Story Crafting:
1. **Create emotional arcs** - build tension and release
2. **Use vivid sensory details** - engage all five senses  
3. **Vary pacing** - mix action with reflection
4. **Create meaningful choices** - each decision should matter
5. **Build toward satisfying endings** - reward player investment

### Quick Actions:
- Use **Export/Import** to save your custom stories
- Try different paths to unlock all **5 achievements**
- Extend the story using the **crafting tools**
""")

st.sidebar.markdown("---")
st.sidebar.info("**Pro Tip**: The best stories balance player agency with compelling narrative structure. Happy storytelling! 📚✨")

# Footer
st.markdown("---")
st.caption("🎭 Narrative Nexus v2.0 | Crafted with magic and code | Explore all paths to discover every ending!")