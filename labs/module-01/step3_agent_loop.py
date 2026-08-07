"""
MODULE 1 · STEP 3 — Watch an agent loop work, in 60 lines of plain Python.

WHAT THIS IS
    Hour 2 said an agent is a model in a loop with tools, memory and a goal:
    Observe -> Plan -> Act -> Reflect, repeating until the goal is met.

    There is no AI model in this file. The loop is the point, and you can read
    every line of it. Swap the decision-making for a model later; the shape of
    the thing does not change.

THE JOB
    A fund's NAV does not match the custodian's. Find out why. This is real
    back-office work — it happens on some fund, somewhere, every single day,
    and it is the kind of task GCC fund administration teams are automating now.

HOW TO RUN
    python3 step3_agent_loop.py

    Nothing to install. No API key. No internet.
"""

# --- the "world" the agent can see -----------------------------------------
FUND_NAV = 104.40           # what our system says
CUSTODIAN_NAV = 104.82      # what the custodian says
UNITS = 1_000_000           # units outstanding

# These are the agent's TOOLS. In a real system each one is a database query
# or an API call. Here they are dictionaries, so you can read them.
TRADES_TODAY = [
    {"stock": "INFY", "side": "BUY", "qty": 5000, "price": 1580.0},
    {"stock": "HDFCBANK", "side": "SELL", "qty": 2000, "price": 1642.0},
]

CORPORATE_ACTIONS = [
    {"stock": "TATAMOTORS", "type": "BONUS", "ratio": "1:1", "processed": False},
]

FX_RATE_USED = 83.20
FX_RATE_CORRECT = 83.20

# The fund holds 1,200 shares of TATAMOTORS. The company issued a 1:1 bonus,
# so the fund is entitled to 1,200 more shares at the ex-bonus price of Rs 350.
HOLDINGS = {"TATAMOTORS": {"qty": 1_200, "ex_bonus_price": 350.0}}

STEP_BUDGET = 4             # the brake. An agent without one runs all night.


def observe():
    gap_per_unit = round(CUSTODIAN_NAV - FUND_NAV, 4)
    total_gap = round(gap_per_unit * UNITS, 2)
    pct = round(gap_per_unit / CUSTODIAN_NAV * 100, 3)
    return {"gap_per_unit": gap_per_unit, "total_gap": total_gap, "pct": pct}


def plan(observation):
    """The agent writes its own to-do list before touching anything."""
    return [
        "check today's trades were booked at the right price",
        "check for unprocessed corporate actions",
        "check the FX rate used for valuation",
    ]


def act(task):
    """Each branch is a tool call. Returns what the tool found."""
    if "trades" in task:
        return {"finding": None,
                "detail": f"{len(TRADES_TODAY)} trades, all booked at traded price"}

    if "corporate actions" in task:
        pending = [c for c in CORPORATE_ACTIONS if not c["processed"]]
        if not pending:
            return {"finding": None, "detail": "no pending corporate actions"}
        ca = pending[0]
        holding = HOLDINGS[ca["stock"]]
        # A 1:1 bonus gives the fund one extra share for every share held.
        # The market price has already fallen to the ex-bonus level, and the
        # custodian has recorded the new shares. We have not. So our NAV is
        # short by (bonus shares x ex-bonus price).
        bonus_shares = holding["qty"]                       # 1:1
        impact = bonus_shares * holding["ex_bonus_price"]
        return {"finding": f"unprocessed {ca['ratio']} bonus on {ca['stock']}",
                "impact_total": impact,
                "detail": (f"{bonus_shares:,} bonus shares not recorded x "
                           f"Rs {holding['ex_bonus_price']:,.2f} ex-bonus price "
                           f"= Rs {impact:,.0f}")}

    if "FX" in task:
        same = FX_RATE_USED == FX_RATE_CORRECT
        return {"finding": None if same else "wrong FX rate",
                "detail": f"rate used {FX_RATE_USED}, correct {FX_RATE_CORRECT}"}

    return {"finding": None, "detail": "no tool for this task"}


def reflect(observation, explained):
    """Is the goal met? Explain the whole gap, or say plainly that you cannot."""
    remaining = round(observation["total_gap"] - explained, 2)
    return remaining, abs(remaining) < 1.0     # within a rupee = explained


def run():
    print("GOAL   Explain why the fund NAV does not match the custodian NAV.\n")

    obs = observe()
    print("OBSERVE")
    print(f"   fund NAV {FUND_NAV}  |  custodian NAV {CUSTODIAN_NAV}")
    print(f"   custodian is higher by Rs {obs['gap_per_unit']} per unit  =  "
          f"Rs {obs['total_gap']:,.0f} "
          f"across {UNITS:,} units  ({obs['pct']}%)\n")

    tasks = plan(obs)
    print("PLAN")
    for i, t in enumerate(tasks, 1):
        print(f"   {i}. {t}")
    print()

    explained = 0.0
    findings = []

    for step, task in enumerate(tasks, 1):
        if step > STEP_BUDGET:
            print("STOP   step budget reached — handing over to a human.")
            return

        result = act(task)
        print(f"ACT {step}  {task}")
        print(f"        -> {result['detail']}")

        if result["finding"]:
            findings.append(result["finding"])
            explained += result.get("impact_total", 0)
            print(f"        -> FOUND: {result['finding']}")

        remaining, done = reflect(obs, explained)
        print(f"REFLECT gap explained so far Rs {explained:,.0f}, "
              f"still unexplained Rs {remaining:,.0f}")

        if done:
            print("\nGOAL MET")
            print("   Cause: " + "; ".join(findings))
            print("   Draft note for the fund accountant:")
            print(f"     Our NAV is Rs {obs['gap_per_unit']} per unit below the "
                  f"custodian. The difference is fully explained by a 1:1 bonus")
            print( "     issue on TATAMOTORS whose 1,200 bonus shares are not yet "
                   "in our books. Process the corporate")
            print( "     action and revalue. No manual NAV adjustment required.")
            print("\n   A HUMAN SIGNS THIS. The agent drafts; it does not send.")
            return
        print()

    print("\nGOAL NOT MET")
    print(f"   Rs {remaining:,.0f} still unexplained after every planned check.")
    print("   Correct behaviour: stop and escalate. Do not invent a reason.")


if __name__ == "__main__":
    run()
    print("""
--------------------------------------------------------------------
WHAT TO NOTICE

  1. The loop only ever calls tools YOU gave it. It cannot touch anything else.
  2. STEP_BUDGET stops it. Every production agent has a step limit, a cost
     limit and an audit log, or it does not go live in a regulated firm.
  3. It reflects after every action, and it is allowed to fail loudly.
  4. The last line of work is a draft for a human, not an instruction to the
     books. That boundary is where accountability still lives.

  TRY THIS: set CORPORATE_ACTIONS[0]["processed"] = True and run it again.
  The agent now explains nothing, and correctly escalates instead of guessing.
""")
