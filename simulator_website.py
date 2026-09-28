import streamlit as st
import random
import math
import json
import os
import time
from decimal import Decimal


# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="Clicker",
    page_icon="🖱️",
    layout="wide"
)


# ==================================================
# VARIABLES
# ==================================================

DEFAULT_DATA = {
    "clicks": 0,

    "permanentMultiplier": 1,

    "multiplier": 1,
    "multiplierCost": 100,

    "frenzyCost": 1000,

    "autoClickerLevel": 0,
    "autoClickerCost": 1000,
    "autoclickerTime": 1000,

    "luckyClickLvl": 1,
    "luckyClickCost": 2500,
    "luckyClickChance": 1,

    "accountUnlocked": False,
    "accountIntrest": 2,
    "criticalAccountIntrest": 10,
    "accountCost": 5000,
    "accountAmount": 0,

    "minigameCost": 5000,

    "interestStarted": False,

    "rebirthCost": 1_000_000,
    "rebirths": 0,

    "gamble5xChance": 1.0,
    "gamble2xChance": 9.0,
    "gambleHalfChance": 40.0,
    "gambleNoneChance": 50.0,

    "lastInterest": time.time(),
    "lastAutoClick": time.time(),

    "frenzyActive": False,
    "frenzyEnd": 0,
    "oldMultiplier": 1,

    "minigameActive": False,
    "minigameFinished": False,
    "placerx": 0.05,
    "placerdirection": 1,
    "targetx": 0.5,

    "gambleResult": "",
    "gambleResultType": "",

    "message": "",
    "messageType": "",

    "shopopened": False,
    "rebirthMenu": False,
    "transactionMenu": None
}


# ==================================================
# SESSION STATE
# ==================================================

for key, value in DEFAULT_DATA.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==================================================
# NUMBER FORMAT
# ==================================================

def formatClicks(number):

    if abs(number) >= 1_000_000_000:

        return f'{Decimal(str(number)):.2E}'

    if isinstance(number, float):

        return f'{number:,.2f}'

    return f'{number:,}'


def formatCost(number):

    if abs(number) >= 1_000_000:

        return f'{Decimal(str(number)):.2E}'

    return f'{number:,}'


# ==================================================
# SAVE
# ==================================================

def saveData():

    data = {

        'clicks':
            st.session_state.clicks,

        'permanentMultiplier':
            st.session_state.permanentMultiplier,

        'rebirths':
            st.session_state.rebirths,

        'multiplier':
            st.session_state.multiplier,

        'multiplierCost':
            st.session_state.multiplierCost,

        'frenzyCost':
            st.session_state.frenzyCost,

        'autoClickerLevel':
            st.session_state.autoClickerLevel,

        'autoClickerCost':
            st.session_state.autoClickerCost,

        'autoclickerTime':
            st.session_state.autoclickerTime,

        'luckyClickLvl':
            st.session_state.luckyClickLvl,

        'luckyClickCost':
            st.session_state.luckyClickCost,

        'luckyClickChance':
            st.session_state.luckyClickChance,

        'accountUnlocked':
            st.session_state.accountUnlocked,

        'accountIntrest':
            st.session_state.accountIntrest,

        'criticalAccountIntrest':
            st.session_state.criticalAccountIntrest,

        'accountCost':
            st.session_state.accountCost,

        'accountAmount':
            st.session_state.accountAmount,

        'minigameCost':
            st.session_state.minigameCost
    }

    with open(
        'save.json',
        'w'
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==================================================
# LOAD
# ==================================================

def loadData():

    try:

        with open(
            'save.json',
            'r'
        ) as file:

            data = json.load(file)

        for key in DEFAULT_DATA:

            if key in data:

                st.session_state[key] = data[key]

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        pass


if not st.session_state.get(
    "loaded",
    False
):

    loadData()

    st.session_state.loaded = True


# ==================================================
# MESSAGE
# ==================================================

def showMessage(
    message,
    messageType="info"
):

    st.session_state.message = message
    st.session_state.messageType = messageType


def displayMessage():

    message = st.session_state.message

    if not message:

        return

    messageType = st.session_state.messageType

    if messageType == "success":

        st.success(message)

    elif messageType == "error":

        st.error(message)

    elif messageType == "warning":

        st.warning(message)

    else:

        st.info(message)


# ==================================================
# CLICK
# ==================================================

def giveclick():

    luckyRoll = random.randint(
        1,
        100
    )

    if luckyRoll <= st.session_state.luckyClickChance:

        amount = (
            2
            * st.session_state.multiplier
            * st.session_state.permanentMultiplier
        )

        st.session_state.clicks += amount

        showMessage(
            f"🍀 LUCKY CLICK! +{formatClicks(amount)} CLICKS!",
            "success"
        )

    else:

        amount = (
            st.session_state.multiplier
            * st.session_state.permanentMultiplier
        )

        st.session_state.clicks += amount

        st.session_state.message = ""


# ==================================================
# MULTIPLIER
# ==================================================

def giveMultiplier():

    if (
        st.session_state.clicks
        >=
        st.session_state.multiplierCost
    ):

        st.session_state.clicks -= (
            st.session_state.multiplierCost
        )

        st.session_state.multiplier += 1

        st.session_state.multiplierCost = math.floor(
            st.session_state.multiplierCost
            * 1.25
        )

        showMessage(
            f"Multiplier is now "
            f"{st.session_state.multiplier}x!",
            "success"
        )

    else:

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )


# ==================================================
# FRENZY
# ==================================================

def givefrenzy():

    if st.session_state.frenzyActive:

        return

    if (
        st.session_state.clicks
        <
        st.session_state.frenzyCost
    ):

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.clicks -= (
        st.session_state.frenzyCost
    )

    st.session_state.frenzyCost = math.floor(
        st.session_state.frenzyCost
        * 1.25
    )

    st.session_state.oldMultiplier = (
        st.session_state.multiplier
    )

    st.session_state.multiplier *= 3

    st.session_state.frenzyActive = True

    st.session_state.frenzyEnd = (
        time.time()
        + 9.775
    )

    showMessage(
        "⚡ FRENZY ACTIVE! 3X MULTIPLIER!",
        "success"
    )


def processFrenzy():

    if not st.session_state.frenzyActive:

        return

    if time.time() >= st.session_state.frenzyEnd:

        st.session_state.multiplier = (
            st.session_state.oldMultiplier
        )

        st.session_state.frenzyActive = False

        st.session_state.frenzyEnd = 0

        showMessage(
            "Frenzy ended!",
            "info"
        )


processFrenzy()


# ==================================================
# AUTO CLICKER
# ==================================================

def lvlUpAutoClicker():

    if (
        st.session_state.clicks
        <
        st.session_state.autoClickerCost
    ):

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.clicks -= (
        st.session_state.autoClickerCost
    )

    st.session_state.autoClickerLevel += 1

    st.session_state.autoClickerCost = math.floor(
        st.session_state.autoClickerCost
        * 1.25
    )

    if st.session_state.autoclickerTime > 100:

        st.session_state.autoclickerTime -= 100

    showMessage(
        f"🤖 AUTO CLICKER LEVEL "
        f"{st.session_state.autoClickerLevel}!",
        "success"
    )


def processAutoClicker():

    if st.session_state.autoClickerLevel <= 0:

        return

    now = time.time()

    elapsed = (
        now
        -
        st.session_state.lastAutoClick
    )

    interval = (
        st.session_state.autoclickerTime
        /
        1000
    )

    if elapsed >= interval:

        amountOfClicks = int(
            elapsed / interval
        )

        amount = (
            amountOfClicks
            * st.session_state.multiplier
            * st.session_state.permanentMultiplier
        )

        st.session_state.clicks += amount

        st.session_state.lastAutoClick = now


processAutoClicker()


# ==================================================
# LUCKY CLICK
# ==================================================

def luckyClick():

    if (
        st.session_state.clicks
        <
        st.session_state.luckyClickCost
    ):

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.clicks -= (
        st.session_state.luckyClickCost
    )

    st.session_state.luckyClickLvl += 1

    st.session_state.luckyClickCost = math.floor(
        st.session_state.luckyClickCost
        * 1.5
    )

    st.session_state.luckyClickChance = min(
        st.session_state.luckyClickChance + 1,
        100
    )

    showMessage(
        f"🍀 Lucky Click Chance: "
        f"{st.session_state.luckyClickChance}%",
        "success"
    )


# ==================================================
# SAVINGS ACCOUNT
# ==================================================

def giveSaving():

    if (
        st.session_state.clicks
        <
        st.session_state.accountCost
    ):

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.clicks -= (
        st.session_state.accountCost
    )

    st.session_state.accountCost = math.floor(
        st.session_state.accountCost
        * 1.25
    )

    if st.session_state.accountUnlocked:

        st.session_state.accountIntrest += random.randint(
            1,
            3
        )

        st.session_state.criticalAccountIntrest += random.randint(
            3,
            6
        )

        showMessage(
            "🏦 SAVINGS ACCOUNT UPGRADED!",
            "success"
        )

    else:

        st.session_state.accountUnlocked = True

        st.session_state.interestStarted = True

        st.session_state.lastInterest = time.time()

        showMessage(
            "🏦 SAVINGS ACCOUNT UNLOCKED!",
            "success"
        )


# ==================================================
# INTEREST
# ==================================================

def giveInterest():

    if not st.session_state.accountUnlocked:

        return

    now = time.time()

    elapsed = (
        now
        -
        st.session_state.lastInterest
    )

    cycles = int(
        elapsed / 60
    )

    if cycles <= 0:

        return

    for _ in range(cycles):

        if st.session_state.accountAmount > 0:

            interestAmount = (
                st.session_state.accountAmount
                *
                st.session_state.accountIntrest
                /
                100
            )

            st.session_state.accountAmount += (
                interestAmount
            )

    st.session_state.lastInterest = now


giveInterest()


# ==================================================
# DEPOSIT
# ==================================================

def depositMoney():

    amount = st.session_state.depositAmount

    if amount <= 0:

        showMessage(
            "ENTER MORE THAN 0!",
            "error"
        )

        return

    if amount > st.session_state.clicks:

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.clicks -= amount

    st.session_state.accountAmount += amount

    st.session_state.transactionMenu = None

    showMessage(
        f"💰 DEPOSITED {formatClicks(amount)} CLICKS!",
        "success"
    )


# ==================================================
# WITHDRAW
# ==================================================

def withdrawMoney():

    amount = st.session_state.withdrawAmount

    if amount <= 0:

        showMessage(
            "ENTER MORE THAN 0!",
            "error"
        )

        return

    if amount > st.session_state.accountAmount:

        showMessage(
            "NOT ENOUGH SAVINGS!",
            "error"
        )

        return

    st.session_state.clicks += amount

    st.session_state.accountAmount -= amount

    st.session_state.transactionMenu = None

    showMessage(
        f"💵 WITHDREW {formatClicks(amount)} CLICKS!",
        "success"
    )


# ==================================================
# RNG
# ==================================================

def doGamble(amount):

    try:

        amount = int(amount)

    except:

        showMessage(
            "ENTER A NUMBER!",
            "error"
        )

        return

    if amount <= 0:

        showMessage(
            "ENTER MORE THAN 0!",
            "error"
        )

        return

    if amount > st.session_state.clicks:

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    totalChance = (
        st.session_state.gamble5xChance
        +
        st.session_state.gamble2xChance
        +
        st.session_state.gambleHalfChance
        +
        st.session_state.gambleNoneChance
    )

    if not math.isclose(
        totalChance,
        100
    ):

        showMessage(
            "CHANCES MUST ADD TO 100%!",
            "error"
        )

        return

    st.session_state.clicks -= amount

    roll = random.random() * 100

    if roll < st.session_state.gamble5xChance:

        reward = amount * 5

        st.session_state.clicks += reward

        st.session_state.gambleResult = (
            f"🍀 LUCKY 5X BONUS!\n"
            f"+{formatClicks(reward)} CLICKS!"
        )

        st.session_state.gambleResultType = "gold"

    elif roll < (
        st.session_state.gamble5xChance
        +
        st.session_state.gamble2xChance
    ):

        reward = amount * 2

        st.session_state.clicks += reward

        st.session_state.gambleResult = (
            f"2X BONUS!\n"
            f"+{formatClicks(reward)} CLICKS!"
        )

        st.session_state.gambleResultType = "success"

    elif roll < (
        st.session_state.gamble5xChance
        +
        st.session_state.gamble2xChance
        +
        st.session_state.gambleHalfChance
    ):

        reward = math.floor(
            amount / 2
        )

        st.session_state.clicks += reward

        st.session_state.gambleResult = (
            f"HALF BACK!\n"
            f"+{formatClicks(reward)} CLICKS!"
        )

        st.session_state.gambleResultType = "warning"

    else:

        st.session_state.gambleResult = (
            "LOSE IT ALL!"
        )

        st.session_state.gambleResultType = "error"


# ==================================================
# MINIGAME START
# ==================================================

def openminigame():

    if st.session_state.minigameActive:

        return

    if (
        st.session_state.clicks
        <
        st.session_state.minigameCost
    ):

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.clicks -= (
        st.session_state.minigameCost
    )

    st.session_state.minigameCost = math.floor(
        st.session_state.minigameCost
        * 1.5
    )

    st.session_state.minigameActive = True

    st.session_state.minigameFinished = False

    st.session_state.placerx = 0.05

    st.session_state.placerdirection = 1

    st.session_state.targetx = random.uniform(
        0.15,
        0.85
    )

    st.session_state.minigameStartTime = time.time()


# ==================================================
# MINIGAME MOVEMENT
# ==================================================

def moveMinigame():

    if not st.session_state.minigameActive:

        return

    if st.session_state.minigameFinished:

        return

    st.session_state.placerx += (
        0.035
        *
        st.session_state.placerdirection
    )

    if st.session_state.placerx >= 0.95:

        st.session_state.placerx = 0.95

        st.session_state.placerdirection = -1

    if st.session_state.placerx <= 0.05:

        st.session_state.placerx = 0.05

        st.session_state.placerdirection = 1


# ==================================================
# MINIGAME CHECK
# ==================================================

def checkminigame():

    if st.session_state.minigameFinished:

        st.session_state.minigameActive = False

        return

    if abs(
        st.session_state.placerx
        -
        st.session_state.targetx
    ) <= 0.10:

        st.session_state.minigameFinished = True

        reward = (
            100
            *
            st.session_state.multiplier
        )

        bonusMultiplier = random.uniform(
            1.05,
            2.05
        )

        bonus = math.floor(
            reward
            *
            bonusMultiplier
        )

        totalReward = (
            reward
            +
            bonus
        )

        st.session_state.clicks += totalReward

        st.session_state.minigameResult = (
            f"🎉 GOOD JOB!\n"
            f"+{formatClicks(totalReward)} CLICKS!"
        )

        st.session_state.minigameResultType = "success"

    else:

        st.session_state.minigameFinished = True

        st.session_state.minigameResult = (
            "❌ MISS!"
        )

        st.session_state.minigameResultType = "error"


# ==================================================
# REBIRTH
# ==================================================

def rebirth():

    if (
        st.session_state.clicks
        <
        st.session_state.rebirthCost
    ):

        showMessage(
            "NOT ENOUGH CLICKS!",
            "error"
        )

        return

    st.session_state.rebirths += 1

    st.session_state.rebirthCost = int(
        st.session_state.rebirthCost
        * 1.5
    )

    st.session_state.permanentMultiplier += 1

    st.session_state.clicks = 1000

    st.session_state.multiplier = (
        st.session_state.permanentMultiplier
    )

    st.session_state.multiplierCost = 100

    st.session_state.frenzyCost = 1000

    st.session_state.frenzyActive = False

    st.session_state.autoClickerLevel = 0

    st.session_state.autoClickerCost = 1000

    st.session_state.autoclickerTime = 1000

    st.session_state.luckyClickLvl = 1

    st.session_state.luckyClickCost = 2500

    st.session_state.luckyClickChance = 1

    st.session_state.accountUnlocked = False

    st.session_state.accountIntrest = 2

    st.session_state.criticalAccountIntrest = 10

    st.session_state.accountCost = 5000

    st.session_state.accountAmount = 0

    st.session_state.interestStarted = False

    st.session_state.minigameCost = 5000

    st.session_state.minigameActive = False

    st.session_state.rebirthMenu = False

    showMessage(
        f"🔄 REBIRTH {st.session_state.rebirths}!\n"
        f"Permanent Multiplier: "
        f"{st.session_state.permanentMultiplier}x",
        "success"
    )


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        linear-gradient(
            135deg,
            #151515,
            #211238,
            #101c45
        );
    }

    .main-title {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .click-display {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        background: rgba(0,0,0,0.55);
        border-radius: 18px;
        padding: 15px;
        margin: 10px 0 25px 0;
    }

    .stat {
        background: rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stat-title {
        font-size: 14px;
        opacity: 0.7;
    }

    .stat-value {
        font-size: 25px;
        font-weight: bold;
    }

    .game-box {
        background: rgba(0,10,50,0.95);
        border-radius: 18px;
        padding: 25px;
        border: 3px solid #00c8ff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# PROCESS
# ==================================================

processFrenzy()

processAutoClicker()

giveInterest()

moveMinigame()


# ==================================================
# TITLE
# ==================================================

st.markdown(
    '<div class="main-title">🖱️ CLICKER</div>',
    unsafe_allow_html=True
)


st.markdown(
    f'''
    <div class="click-display">
        {formatClicks(st.session_state.clicks)}
    </div>
    ''',
    unsafe_allow_html=True
)


displayMessage()


# ==================================================
# MAIN CLICK BUTTON
# ==================================================

left, center, right = st.columns(
    [1, 2, 1]
)

with center:

    if st.button(
        "🖱️ CLICK FOR POINTS",
        use_container_width=True,
        type="primary"
    ):

        giveclick()

        saveData()

        st.rerun()


# ==================================================
# STATS
# ==================================================

st.divider()

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f'''
        <div class="stat">
            <div class="stat-title">
                MULTIPLIER
            </div>
            <div class="stat-value">
                {st.session_state.multiplier}x
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f'''
        <div class="stat">
            <div class="stat-title">
                PERMANENT
            </div>
            <div class="stat-value">
                {st.session_state.permanentMultiplier}x
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f'''
        <div class="stat">
            <div class="stat-title">
                LUCKY CHANCE
            </div>
            <div class="stat-value">
                {st.session_state.luckyClickChance}%
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f'''
        <div class="stat">
            <div class="stat-title">
                REBIRTHS
            </div>
            <div class="stat-value">
                {st.session_state.rebirths}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


# ==================================================
# SHOP
# ==================================================

st.divider()

st.header("🏪 SHOP")


s1, s2 = st.columns(2)

with s1:

    st.subheader("➕ MULTIPLIER")

    st.write(
        f"Multiplier: "
        f"**{st.session_state.multiplier}x**"
    )

    st.write(
        f"Cost: "
        f"**{formatCost(st.session_state.multiplierCost)}**"
    )

    if st.button(
        "➕ +1 MULTIPLIER",
        use_container_width=True
    ):

        giveMultiplier()

        saveData()

        st.rerun()


with s2:

    st.subheader("⚡ FRENZY")

    if st.session_state.frenzyActive:

        remaining = max(
            0,
            st.session_state.frenzyEnd
            -
            time.time()
        )

        st.warning(
            f"⚡ FRENZY ACTIVE — "
            f"{remaining:.1f}s"
        )

    else:

        st.write(
            f"Cost: "
            f"**{formatCost(st.session_state.frenzyCost)}**"
        )

        if st.button(
            "⚡ FRENZY",
            use_container_width=True
        ):

            givefrenzy()

            saveData()

            st.rerun()


s3, s4 = st.columns(2)

with s3:

    st.subheader("🤖 AUTO CLICKER")

    st.write(
        f"Level: "
        f"**{st.session_state.autoClickerLevel}**"
    )

    st.write(
        f"Interval: "
        f"**{st.session_state.autoclickerTime} ms**"
    )

    st.write(
        f"Cost: "
        f"**{formatCost(st.session_state.autoClickerCost)}**"
    )

    if st.button(
        "🤖 UPGRADE AUTO CLICKER",
        use_container_width=True
    ):

        lvlUpAutoClicker()

        saveData()

        st.rerun()


with s4:

    st.subheader("🍀 LUCKY CLICK")

    st.write(
        f"Level: "
        f"**{st.session_state.luckyClickLvl}**"
    )

    st.write(
        f"Chance: "
        f"**{st.session_state.luckyClickChance}%**"
    )

    st.write(
        f"Cost: "
        f"**{formatCost(st.session_state.luckyClickCost)}**"
    )

    if st.button(
        "🍀 UPGRADE LUCKY CLICK",
        use_container_width=True
    ):

        luckyClick()

        saveData()

        st.rerun()


# ==================================================
# SAVINGS
# ==================================================

st.divider()

st.header("🏦 SAVINGS ACCOUNT")


if not st.session_state.accountUnlocked:

    st.write(
        "Buy the Savings Account to start earning interest."
    )

    st.write(
        f"Cost: "
        f"**{formatCost(st.session_state.accountCost)}**"
    )

    if st.button(
        "🏦 BUY SAVINGS ACCOUNT",
        use_container_width=True
    ):

        giveSaving()

        saveData()

        st.rerun()

else:

    a1, a2, a3 = st.columns(3)

    with a1:

        st.metric(
            "SAVINGS",
            formatClicks(
                st.session_state.accountAmount
            )
        )

    with a2:

        st.metric(
            "INTEREST",
            f"{st.session_state.accountIntrest}%"
        )

    with a3:

        st.metric(
            "CRITICAL INTEREST",
            f"{st.session_state.criticalAccountIntrest}%"
        )

    st.write(
        f"Upgrade Cost: "
        f"**{formatCost(st.session_state.accountCost)}**"
    )

    if st.button(
        "🏦 UPGRADE ACCOUNT",
        use_container_width=True
    ):

        giveSaving()

        saveData()

        st.rerun()

    d1, d2 = st.columns(2)

    with d1:

        depositAmount = st.number_input(
            "Deposit Amount",
            min_value=0,
            step=1,
            key="deposit_input"
        )

        if st.button(
            "💰 DEPOSIT",
            use_container_width=True
        ):

            st.session_state.depositAmount = (
                depositAmount
            )

            depositMoney()

            saveData()

            st.rerun()

    with d2:

        withdrawAmount = st.number_input(
            "Withdraw Amount",
            min_value=0,
            step=1,
            key="withdraw_input"
        )

        if st.button(
            "💵 WITHDRAW",
            use_container_width=True
        ):

            st.session_state.withdrawAmount = (
                withdrawAmount
            )

            withdrawMoney()

            saveData()

            st.rerun()


# ==================================================
# MINIGAME
# ==================================================

st.divider()

st.header("🎮 MINIGAME")

st.write(
    f"Entry Cost: "
    f"**{formatCost(st.session_state.minigameCost)}**"
)


if not st.session_state.minigameActive:

    if st.button(
        "🎮 OPEN MINIGAME",
        use_container_width=True
    ):

        openminigame()

        saveData()

        st.rerun()

else:

    st.markdown(
        '<div class="game-box">',
        unsafe_allow_html=True
    )

    st.subheader(
        "🎯 HIT THE TARGET!"
    )

    st.write(
        "Click the button when the marker "
        "is over the yellow target."
    )

    position = st.session_state.placerx

    target = st.session_state.targetx

    st.progress(
        min(
            1.0,
            max(
                0.0,
                position
            )
        )
    )

    st.write(
        f"Marker Position: "
        f"**{position * 100:.1f}%**"
    )

    st.write(
        f"Target Position: "
        f"**{target * 100:.1f}%**"
    )

    if not st.session_state.minigameFinished:

        if st.button(
            "🎯 CLICK!",
            use_container_width=True
        ):

            checkminigame()

            saveData()

            st.rerun()

    else:

        result = st.session_state.get(
            "minigameResult",
            ""
        )

        if st.session_state.get(
            "minigameResultType"
        ) == "success":

            st.success(result)

        else:

            st.error(result)

        if st.button(
            "CLOSE MINIGAME",
            use_container_width=True
        ):

            st.session_state.minigameActive = False

            st.session_state.minigameFinished = False

            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# RNG
# ==================================================

st.divider()

st.header("🎲 RNG BONUS")


r1, r2 = st.columns(2)

with r1:

    st.write(
        f"🍀 **{st.session_state.gamble5xChance}%** — 5X"
    )

    st.write(
        f"🟢 **{st.session_state.gamble2xChance}%** — 2X"
    )

with r2:

    st.write(
        f"🟠 **{st.session_state.gambleHalfChance}%** — HALF"
    )

    st.write(
        f"🔴 **{st.session_state.gambleNoneChance}%** — NONE"
    )


gambleAmount = st.number_input(
    "Amount to gamble",
    min_value=0,
    step=1,
    key="gamble_amount"
)


if st.button(
    "🎲 ROLL",
    use_container_width=True
):

    doGamble(
        gambleAmount
    )

    saveData()

    st.rerun()


if st.session_state.gambleResult:

    resultType = (
        st.session_state.gambleResultType
    )

    if resultType == "gold":

        st.success(
            st.session_state.gambleResult
        )

    elif resultType == "success":

        st.success(
            st.session_state.gambleResult
        )

    elif resultType == "warning":

        st.warning(
            st.session_state.gambleResult
        )

    else:

        st.error(
            st.session_state.gambleResult
        )


# ==================================================
# REBIRTH
# ==================================================

st.divider()

st.header("🔄 REBIRTH")


r1, r2 = st.columns(2)

with r1:

    st.write(
        f"Requirement: "
        f"**{formatCost(st.session_state.rebirthCost)} CLICKS**"
    )

    st.write(
        f"Your Clicks: "
        f"**{formatClicks(st.session_state.clicks)}**"
    )

with r2:

    st.write(
        f"Current Permanent Multiplier: "
        f"**{st.session_state.permanentMultiplier}x**"
    )

    st.write(
        f"After Rebirth: "
        f"**{st.session_state.permanentMultiplier + 1}x**"
    )


if st.session_state.clicks >= st.session_state.rebirthCost:

    st.success(
        "READY TO REBIRTH!"
    )

else:

    needed = (
        st.session_state.rebirthCost
        -
        st.session_state.clicks
    )

    st.warning(
        f"NEED {formatCost(needed)} MORE CLICKS"
    )


if st.button(
    "🔄 OPEN REBIRTH MENU",
    use_container_width=True
):

    st.session_state.rebirthMenu = (
        not st.session_state.rebirthMenu
    )

    st.rerun()


if st.session_state.rebirthMenu:

    st.divider()

    st.subheader(
        "🔄 REBIRTH CONFIRMATION"
    )

    st.write(
        "Reset your progress for a permanent boost."
    )

    st.info(
        f"Requirement: "
        f"{formatCost(st.session_state.rebirthCost)} clicks"
    )

    st.info(
        f"HAVE: "
        f"{st.session_state.permanentMultiplier}x\n\n"
        f"GET: +1x\n\n"
        f"AFTER: "
        f"{st.session_state.permanentMultiplier + 1}x"
    )

    if st.session_state.clicks >= st.session_state.rebirthCost:

        if st.button(
            "🔄 CONFIRM REBIRTH",
            use_container_width=True,
            type="primary"
        ):

            rebirth()

            saveData()

            st.rerun()

    else:

        st.button(
            "🔄 CONFIRM REBIRTH",
            disabled=True,
            use_container_width=True
        )

    if st.button(
        "CANCEL",
        use_container_width=True
    ):

        st.session_state.rebirthMenu = False

        st.rerun()


# ==================================================
# SAVE
# ==================================================

st.divider()

if st.button(
    "💾 SAVE GAME",
    use_container_width=True
):

    saveData()

    st.success(
        "GAME SAVED!"
    )


# ==================================================
# AUTO REFRESH
# ==================================================

if (
    st.session_state.autoClickerLevel > 0
    or st.session_state.accountUnlocked
    or st.session_state.frenzyActive
):

    time.sleep(0.5)

    st.rerun()