# Documentation Analysis Report

**Analyzed URL:** https://help.moengage.com/hc/en-us/articles/16768530490132-Android-Push-Permission-and-Reachability
**Analysis Timestamp:** 2025-06-01T10:07:40.015455+00:00

**Overall Score:** Fair

---

## Readability Analysis

**Score:** Poor
**Assessment:** This document is difficult for a non-technical business user to understand because it contains too much technical jargon and assumes a level of familiarity with Android development concepts that this audience likely does not possess. The document frequently dives into implementation details without providing sufficient context or simplification for a general audience.

**Issues Found:**
- "Push notifications permission is an app-level permission that your app gets on a user's device."
- "they will get delivered in the background to your app silently."
- "While apps are automatically granted permission to send notifications for Android 12 and lower versions, Android 13 and higher OS versions require the apps to request permission from users before sending notifications."
- "Android has introduced runtime permission for users to grant the push permission"
- "Apps targeting Android 13 or higher Apps targeting Android 12 (compatibility mode)"
- "As per Google Play’s target API level requirement, from August 31, 2023: New apps must target Android 13 (API level 33) or higher, except for Wear OS apps, which must target Android 11 (API level 30). App updates must target Android 13 or higher and adjust for behavioral changes in Android 13, except for Wear OS apps, which must target Android 11."
- "When an app creates a notification channel for the first time, the user will be prompted to grant permission."
- "To enable Android to push notification Opt-in/Opt-out tracking, upgrade to MoEngage Core SDK version 12.3.01 and above. MoEngage SDK tracks the device's opt-in status by default. The opt-in status of the user’s devices will be can be tracked by the “Reachability Push Android” user attribute."
- "Opt-in/opt-out tracking is supported on MoEngage Core SDK version 12.3.01 and above."
- "These events will be generated only when the Opt-in status of a device changes or a user explicitly confirms the permission. The default state of a device will not trigger a Subscribed/unsubscribed to push event."
- "In a Self-handled Opt-in, developers can directly call the Android notification permission prompt like any other runtime permission."
- Terms like 'API level', 'runtime permission', 'SDK version' will be unfamiliar and confusing.

**Suggestions:**
- Replace technical terms like 'app-level permission' with simpler explanations like 'permission for the app to send notifications'.
- Instead of 'delivered in the background to your app silently', explain that the user won't see the notification.
- Rephrase sentences to focus on the user experience rather than technical implementation. For example, instead of "Android has introduced runtime permission for users to grant the push permission", say something like "Starting with newer Android phones, users now have more control over whether they want to receive notifications from an app."
- Avoid mentioning specific 'API levels' or 'SDK versions' unless absolutely necessary. If you must, provide a brief explanation of what they mean in plain language.
- Explain the importance of 'Opt-in/Opt-out tracking' in terms of user engagement and campaign effectiveness. Focus on the benefit of tracking rather than the technical details.
- Simplify the language around the aggressive, balanced, and conservative strategies. Use more relatable examples and avoid phrases like 'self-handled opt-in method'.
- Use visuals (e.g., flowcharts) to illustrate the opt-in process and the different strategies.

---

## Structure Analysis

**Score:** Fair
**Assessment:** The document covers important information about Android push permissions, but its structure is somewhat disorganized, hindering readability and navigability. The frequent repetition and lack of clear hierarchy make it challenging to quickly grasp the key concepts.

**Counts:**
  - H1: 1
  - H2: 2
  - H3: 1
  - Paragraphs: 71
  - Lists: 12

**Sub-Analysis:**
  - Headings: The heading structure is very shallow, mostly relying on H2 and H3 headings. The H1 is suitable for the entire document, but the rest is not deep enough. Some sections that could benefit from being in a structured list are presented as paragraphs, affecting readability.
  - Paragraphs/Lists: Paragraphs are frequently short, sometimes only one or two sentences, which disrupts the flow. Lists are used effectively when presenting specific actions or attributes but are underutilized in other areas where they could enhance clarity. Repetitive information is present in numerous paragraphs.

**Flow & Navigation Assessment:** The logical flow is weakened by repetition and a lack of clear transitions between topics. Navigation is difficult due to the shallow heading structure and the absence of a table of contents or other navigational aids.

**Issues Found:**
- Shallow heading structure makes it difficult to navigate.
- Frequent repetition of information leads to redundancy and reader fatigue.
- Paragraphs are often too short and fragmented.
- Lack of clear transitions between topics.
- Inconsistent use of lists for related information.
- Overuse of "info" callouts for general information, diluting their impact.

**Suggestions:**
- Implement a more detailed heading structure (H1, H2, H3, H4 where applicable) to create a clear hierarchy.
- Consolidate repetitive information and rephrase for clarity.
- Combine short paragraphs into longer, more cohesive paragraphs.
- Add transition sentences between sections to improve flow.
- Use lists to present related information concisely and improve readability.
- Create a table of contents or other navigational aids to enhance discoverability.
- Reduce the use of 'info' callouts. Reserve them for only the most critical pieces of information.
- Consider breaking the document into separate, more focused articles. The 'Improving Opt-In Rates' section, especially, could be a separate article.

---

## Completeness Analysis

**Score:** Fair
**Assessment:** The article provides a decent overview of Android push permission management, especially regarding Android 13. However, the examples are repetitive, lack visual aids, and could be significantly more practical and tailored to specific development scenarios.

**Issues Found:**
- The article repeats the same implementation details across different strategies (Aggressive, Balanced, Conservative).
- There are no code examples illustrating how to implement the One-Step Opt-in or Self-Handled Opt-in methods in actual Android code.
- The article mentions a Reachability Dashboard but lacks any screenshot or visual representation of it.
- The use-case examples are very high level. More concrete examples tailored to different app categories would be beneficial.
- The meaning of "Implementation Details" is unclear. It's referred to multiple times without providing a direct link.
- The description of Self-handled Opt-in is brief and lacks practical details about notifying the SDK of the notification count, which sounds important.
- There's no information or examples showing how to use MoEngage's SDK to trigger the native Android permission request prompt.
- The description of tracking opt-in rate relies on navigating MoEngage dashboards but lacks screenshots to guide the user, and the description is somewhat convoluted.
- The article talks about In-app notifications but does not showcase the UI of setting up the "pre-permission messages" using In-App campaigns.
- It is unclear what "notification count" refers to in the context of Self-Handled Opt-in and how it should be handled.

**Suggestions:**
- Consolidate the shared implementation details (First permission method, Follow-up method, Use case-based) into a single section and then reference it from each strategy, highlighting the differences in a separate paragraph.
- Add code snippets demonstrating how to use the MoEngage SDK to implement One-Step and Self-Handled Opt-ins, including error handling and best practices.
- Include a screenshot of the Reachability Dashboard, highlighting key metrics and how to interpret them.
- Provide more specific use-case examples for each strategy, tailored to different app categories (e.g., e-commerce, gaming, social media).
- Replace "Implementation Details" with a direct link to a relevant section or document that provides the necessary details.
- Expand the Self-Handled Opt-in section with more detailed instructions and explain how and why the SDK needs to be notified of the "notification count."
- Provide clear instructions and code examples showing how to trigger the native Android permission request prompt using the MoEngage SDK.
- Add screenshots to the section on tracking opt-in rates on the MoEngage dashboard to guide users through the process step-by-step.
- Include screenshots of how the In-App notifications are set up for pre-permission messages to clarify this process.
- Include a troubleshooting section to address common issues developers might encounter when implementing these features, such as handling edge cases or debugging permission-related problems.

---

## Style Analysis

**Score:** Fair
**Assessment:** The document provides a lot of useful information but could be improved in terms of clarity, conciseness, and action-oriented language. It often repeats information and lacks strong calls to action.

**Sub-Analysis:**
  - Voice & Tone: The voice is generally helpful, but at times becomes slightly technical and formal. A more conversational tone would be beneficial.
  - Clarity & Conciseness: The document suffers from some repetition and could be more concise. Some sentences are unnecessarily complex. It defines some Android versions that could be easily explained in plain terms.
  - Action-Oriented Language: The document provides some guidance, but could use stronger verbs and more explicit calls to action to guide the user through the process. It lacks concrete actionable items.

**Issues Found:**
- Repetitive explanations about what happens when a user grants or denies permission.
- Passive voice: "...will be prompted to grant permission" can be made active.
- Vague phrasing: "Apps that run in compatibility mode...will still request permission" could be more direct.
- Use of jargon: "target API level requirement" could be simplified for wider audience.
- Lack of strong action verbs: "You can employ any of the methods mentioned below to request permission" is weak.
- Inconsistent capitalization (e.g., 'Push' sometimes and sometimes not).
- Redundant language: "Users who are already opted-in"

**Suggestions:**
- Consolidate repeated explanations about permission granting/denial into a single, clear statement.
- Replace passive voice constructions with active ones to make sentences more direct.
- Use simpler language and avoid jargon whenever possible. Replace "target API level requirement" with "minimum API level required".
- Include stronger action verbs, such as "Implement the following steps to..."
- Use consistent capitalization for terms like "Push notifications".
- Rephrase redundant language to be more concise. Change 'Users who are already opted-in' to 'Opted-in users'.
- Replace "You can employ any of the methods mentioned below to request permission" with "Use these methods to request permission"
- Add more specific instructions on *how* to perform the described actions (e.g., 'Click the X button to navigate to Y').

---

