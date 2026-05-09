# Step 3 — Publish the Data Agent to Microsoft Teams

**Goal:** Make `RM_Copilot` reachable as a Teams chat / app for the RM team.

## 3.1 Prerequisites

- ✅ Agent published in Step 2.
- ✅ You have Microsoft 365 with Microsoft Teams.
- ✅ Your tenant allows installing Fabric Data Agents in Teams (admin policy).
- ✅ The RM users you want to give access to are members of the Fabric workspace, with at least **Viewer** on the Data Agent.

## 3.2 Trigger Teams publishing

Open the **`RM_Copilot`** Data Agent and click **Share / Publish → Microsoft Teams** (the wording may differ slightly by tenant; in some it's **Channels → + Add → Teams**).

You'll be prompted for:

| Field | Value |
|---|---|
| App display name | `RM Copilot — ผู้ช่วย RM` |
| Short description | `Lead-qualification assistant for the RM team` |
| Long description | (paste the Description from Step 1.3) |
| Icon (192×192) | Use any bank-branded icon |
| Allowed audience | `Specific people` → add the RM team members or a security group |

`[screenshot: Publish-to-Teams dialog]`

Click **Publish**.

## 3.3 Install in Teams

Tenant-wide approval may be needed by an admin (one-time). Once approved:

1. Open Microsoft Teams.
2. Click **Apps → Built for your org** (or search `RM Copilot`).
3. Click **Add**.
4. Open a chat with the bot.

`[screenshot: Teams Apps panel showing RM Copilot]`

## 3.4 Smoke-test in Teams

Send a message to the bot:

> *แสดง Mass-Affluent ในกรุงเทพที่ตอบ campaign บัตรเครดิตในรอบ 90 วันล่าสุดและยังไม่มีบัตรเครดิต*

Expected: a Markdown table reply with `customerId`, `fullName`, `province`, `segmentName`, `monthlyIncomeThb`, `lastResponseDate`. Same look-and-feel as the Test tab in Step 2.

`[screenshot: Teams chat with the bot showing tabular answer]`

## 3.5 Add to a team channel (group use)

To let the whole RM team consult it together:

1. In a Teams channel, click **+ → Add an app**.
2. Choose **RM Copilot**.
3. Pin the tab.

Now any RM can `@mention` the bot inside the team channel for shared lead-qualification sessions.

`[screenshot: Channel tab showing RM Copilot pinned]`

## 3.6 Governance checklist

| Item | Action |
|---|---|
| Audit log | Confirm Teams chats with the bot are captured in Purview audit |
| DLP | Add a DLP policy on the Fabric workspace if your tenant allows it |
| Access | Review Data Agent permissions monthly — only the RM security group |
| Versioning | When you re-publish a new agent version, announce it in the channel |

## 3.7 Done

Step 3 complete. If your bank uses **Microsoft 365 Copilot**, continue to [Step 4](step-04-optional-copilot-studio.md) to wire the agent into Copilot Studio so RMs can call it from inside M365 Copilot. Otherwise, **Lab 3 is done** — congrats! 🎉
