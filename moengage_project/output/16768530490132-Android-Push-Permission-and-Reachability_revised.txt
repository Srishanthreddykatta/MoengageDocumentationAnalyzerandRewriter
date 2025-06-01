# User Guide

## Campaigns and Channels

### Mobile Push

#### Getting Started with Mobile Push

##### Android Push Permission and Reachability

## Overview - Push Permissionlink

Push notification permission is a setting on a user's device that allows your app to display notifications. Without this permission, users won't see the push notifications you send; the notifications will be delivered to the app in the background without any visible alert.

## How Does Push Permission Work?link

On Android 12 and earlier, apps are automatically granted permission to send notifications. However, starting with Android 13, apps must request permission from users before sending notifications. This gives users more control over which apps can send them notifications.

*   **Android 12 and lower:** Apps are automatically allowed to send notifications. Users are "opted-in" by default and don't need to grant specific permission.
*   **Android 13 and higher:** Apps must ask for permission to send notifications. When a user installs or updates an app on Android 13 or higher, the app cannot send notifications until the user grants permission.

Android now includes a system where users can grant or deny permission for push notifications.

*   **If the user grants permission:** The app can send notifications.
*   **If the user denies or ignores the request:** The app cannot send notifications.

The image illustrates how Push permissions are requested from users by an app (Trip Planner).
Users can still go to the app's notification settings and change the permission, similar to the older Android versions.

### Push Permissions on Different Android Versions

The way push permissions work depends on which version of Android your app is designed for:

*   **Apps targeting Android 13 or higher:** These apps have the most control over when and how the permission request is displayed to the user.
*   **Apps targeting Android 12 (compatibility mode):** These apps still need permission on Android 13, but the permission request is triggered automatically when the app creates its first notification channel.

#### Apps Targeting Android 13 or Higher

Apps can control when and where the prompt to grant permission is displayed to a user.
If the user grants permission, the app will be able to send notifications to the user.
If the user denies or ignores permission, the app will not be able to send notifications to the user.
If the user explicitly denies permission twice, the app will not be able to prompt the user again unless the user reinstalls the app

#### Apps Targeting Android 12 (Compatibility Mode)

Apps that run in compatibility mode (targeting Android 12 or lower) on Android 13 will still request permission for notifications, but the user will be prompted to grant permission when the app creates its first notification channel ()
Here's how push notification permission works in Android 13 compatibility mode:

When an app creates a notification channel for the first time, the user will be prompted to grant permission.
If the user grants permission, the app will be able to send notifications to the user.
If the user denies or ignores permission, the app will not be able to send notifications to the user. After this, the user will not be prompted again unless the user reinstalls the app.

#### Permission Reset and OS Upgrades

This permission is reset on every reinstall and clear data. This permission is retained on OS upgrades with one exception. When the user upgrades the device from Android 12 to Android 13:

*   **If the app *did not* have permission in Android 12:** After upgrading to Android 13, the app will not be able to send notifications until the user grants permission.
*   **If the app *had* permission in Android 12:** After upgrading to Android 13, the app will be able to send notifications via a temporary grant which remains till the user opens the app for the first time after the upgrade. After the user opens the app, the permission resets, and the app will not be able to send notifications until the user grants permission.

info

Information
As per Google Play’s target API level requirement, from August 31, 2023:

New apps must target Android 13 (API level 33) or higher, except for Wear OS apps, which must target Android 11 (API level 30).
App updates must target Android 13 or higher and adjust for behavioral changes in Android 13, except for Wear OS apps, which must target Android 11.

## Tracking Push Permissionslink

To track whether users have granted or denied push notification permission on Android, upgrade to MoEngage Core SDK version 12.3.01 or higher. The MoEngage SDK automatically tracks this status. This allows you to understand how many users are reachable via push notifications and tailor your campaigns accordingly. The opt-in status of the user’s devices will be can be tracked by the “Reachability Push Android” user attribute.

Tracking opt-in/opt-out is essential for understanding user engagement and campaign effectiveness. It allows you to:

*   Measure the impact of your opt-in strategies.
*   Segment your audience based on their notification preferences.
*   Avoid sending notifications to users who have opted out, improving user experience.

### Tracking Push Permission Status at a User Levellink

The `Reachability Push Android` attribute indicates a user's push notification status:

| Reachability Push Android attribute value | Reachability Description                                                                                                                                                   |
| :---------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 202 - Not reachable due to Opt-out       | This is the reachability value for any user who has opted out of receiving push notifications on all of their Android devices eligible for Push. These users are no longer considered reachable and will not be targeted for campaigns. |
| 201 - Reachable and opted in             | This is the reachability value for any user who has opted in to receive push notifications on at least one of their Android devices.                                         |
| 200 - Reachable and opt-in status unknown | This is the reachability value for users whose opt-in/opt-out preferences are not being tracked because these users are on the older SDK version. These users will be considered reachable and will be attempted for sending push notifications, but some of these users may be opted-out and will not be able to see notifications. Opt-in/opt-out tracking is supported on MoEngage Core SDK version 12.3.01 and above.                                                |

### Tracking Changes in Push Permission at a User Levellink

The following events are tracked when a user's Android push permission changes:

| Name                  | Description                                                                                                                                                          | Platform   |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- |
| Subscribed to Push    | Tracked when a user subscribes to Push Notifications.                                                                                                               | Android    |
| Unsubscribed to Push | Tracked when a user changes push permission for a device from Subscribed to Unsubscribed Note: This event will not be generated for devices where the permission is denied by default. | Android    |

info

Information
These events will be generated only when the Opt-in status of a device changes or a user explicitly confirms the permission. The default state of a device will not trigger a Subscribed/unsubscribed to push event.
Example - For Android 12 and below devices, the device is opted-in by default. This will not trigger a Subscribed to push event. For Android 13, the user is opted out by default and it will not trigger an Unsubscribed to push event. However, if you request push permission to the user via the native prompt and the user blocks permission, you will get an Unsubscribed to push event.

### Tracking Push Permission Trends Over Timelink

The Reachability Dashboard at MoEngage shows you the reachability trends of all users who opted in to receive your Push notifications and those who have not. You can access the Reachability Dashboard by navigating to Dashboards > Reachability.

For more information, refer to Push Reachability Dashboard.
### Tracking Opt-In Rate of Android 13 Userslink
Since the users have multiple devices, data for a specific OS version is not available.
The steps to track the Opt-in rate for users who are active on your app in the last 60 days are described belowd.

Navigate to Analytics -> Behavior on the MoEngage Dashboard.
In the Events & filters section, select users who did an App/Site Opened event and whose OS version is 33.
In the Filter Users section, select the Filter users by option.
Select the filter condition for the User property Reachability Push Android as in the following [201-Reachable and opted in, 202- Reachable but opted out].
In the Behavior Options, choose the Analysis type as Unique users, Compare by as Reachability Push Android, and the Duration as last 2 months.
Select the Pie Chart visualization in the Behavior Chart section. A sample image for the filter conditions chosen is shown below. The percentage of users with 201 as the ratio should give you the Opt-in rate for Android 13 users only. You can modify the query to get the opt-in rates for users on other OS versions.

## Improving Opt-In Rateslink

To maximize the number of users who allow push notifications, it's crucial to target Android 13 (API level 33) or higher as soon as possible. This allows you to take advantage of the greater control and flexibility offered by the new permission system. Targeting older versions limits your ability to request permission in a way that's relevant to your app's functionality.

## Opt-In Methodslink

Use these methods to request permission to send Push notifications:

*   Two-Step Opt-in
*   One-Step Opt-in
*   Self-Handled Opt-in

### Two-Step Opt-in

A two-step opt-in involves asking for permission in two stages. First, you provide context to the user about why they should allow push notifications. Then, you direct them to the notification settings to enable notifications for your app.

#### Prerequisite for two-step opt-in
Integrate In-app notifications in Moengage SDK 12.6.00 and above and InApp version 6.5.0 or above, refer to the release notes for compatible version of the core SDK.
#### Pre-permission messages

Using In-app notifications, you can create pre-permission messages that can give the context to the user on why they should allow Push notifications for your app. Since you cannot trigger the Android native push prompt if the user explicitly denies permission twice, this method also helps you avoid showing the Android native push prompt unnecessarily, and you can reach out to the user again.

#### Campaign setup for showing the two-step opt-in prompt
Actions

Request notification permissionIf the user is eligible, this action triggers the Android native notification permission. If the user is not eligible because they have already declined the prompt multiple times or are on a lower OS version, they will be redirected to the application notification settings screen where the user can manage notification permission
Navigate to Notification SettingsThis action takes the user to the application notification settings screen, where the user can manage notification permission

#### Segmentation
Unless there is a specific use case to filter out a segment of users, we recommend using “All users” as the segmentation condition. Moegnage automatically manages the following cases:

Irrelevant usersFor In-app notifications that contain any of the above actions, Moengage will automatically filter out irrelevant users e.g.

Users who are already opted-in
Users who are on older SDK version where Opt-in permissions actions is not supported

Android 12 or lower usersThese actions automatically select the right behavior for opted-out users based on the OS version. Android 12 or lower users would be taken to the application notification settings screen, where the user can manage notification permission

#### Priority
Campaigns with the above actions are automatically set to Critical-functional priority, which prioritizes them over other campaigns with the same trigger condition
#### Minimum delay
You can choose to add a minimum delay to nudge the users every few days instead of asking them for permission in every session

### One-Step Opt-in

A one-step opt-in involves directly asking the user for permission to send push notifications using the standard Android permission prompt. You can trigger this prompt at key moments in the user journey based on your business logic. The MoEngage SDK provides APIs to display the Android permission request or navigate the user to the notification settings. For more information, refer to Notification-Runtime-Permissions.

### Self-Handled Opt-in

In a self-handled opt-in, developers directly trigger the Android notification permission prompt, similar to any other runtime permission. However, it's crucial to notify the SDK of the notification count for other methods to function properly.
Unless you are confident about your implementation of self-handled opt-in, we would recommend using One-step Opt-in as a method instead since it tracks the number of times the permission is displayed to the user and implicitly understands the next action when called.

## Recommended Strategieslink

Use these methods to request permission to send Push notifications to users. Here are a few recommended strategies that you can implement to get the optimal number of users for Push notifications.

*   Aggressive
*   Balanced
*   Conservative
*   Use Case Only

Each strategy involves a combination of the opt-in methods described above.

### Shared Implementation Details

The following elements are common to multiple opt-in strategies:

*   **First permission method:** This refers to how you request permission the first time a user logs in. The specific method varies depending on the strategy.
*   **Follow-up method:** This involves using in-app notifications to encourage users to grant push permission. This typically involves a two-step opt-in campaign with a delay between each request.
    *   **Segmentation:** All users
    *   **Trigger:** Homepage screen
    *   **Minimum delay between campaigns:** 10 days
*   **Use case-based:** This involves triggering a two-step opt-in campaign based on specific user actions or events, such as completing a checkout, viewing a thank-you screen, or subscribing to a program.

### Aggressive

*   **Target audience:** Apps that heavily rely on push notifications for user engagement (e.g., news apps, social media).

*Implementation*
Use the following implementation:

First permission method: Refers to the opt-in or permission request that is sent to users the very first time they log in. Depending on the strategy you choose, the way you seek the first permission may differ.Use a self-handled opt-in method to trigger notifications requesting push permission directly on every app open. In this approach, the notification prompt is displayed until the user clicks Don’t allow twice.

Follow-up method: Follow-up in-app notifications are sent as a nudge to encourage users to grant push permission or opt-in to receive push notifications from the app. To use this method, you must space out a two-step opt-in campaign regularly with a few days delay between campaigns. You can set up the campaign by adding the push notification to a navigable screen. After the user clicks the notification, you can trigger a single-step opt-in push notification. The follow-up campaign should follow these conditions:

Segmentation: All users
Trigger: Homepage screen
Minimum delay between 2 campaigns: 10 days

Use case-based: This is a trigger-based two-step opt-in campaign. For example, you could set up an in-app campaign that is triggered on certain events such as the “Checkout complete” event, Thank-you screen, Upcoming events screen, and “Subscribed to program”. You can select the event trigger based on the event of your choice and add the segmentation criteria as All users.

For more details, refer to Implementation Details.

*Insights from early data*

We observed that this gives the highest opt-in rate for some apps. However, this has a tendency to annoy users leading to uninstalls, and follow-up campaigns have poor performance because the user must go to settings to give push permission.

This strategy uses a **self-handled opt-in** to request push permission every time the app is opened. It displays the notification prompt until the user taps "Don't allow" twice.  It also uses a two-step opt-in campaign.

*   **Example Use Cases:**
    *   *E-commerce app:* Prompting users for notifications about flash sales and exclusive offers.
    *   *Social media app:* Requesting permission to send notifications about new followers and mentions.

### Balanced

*   **Target audience:** Apps where most users are not sensitive about permissions (e.g., utility apps, productivity tools).

Examples

The following are some examples of where this strategy can be employed:
With this flow, you will get a:

direct prompt on the first install
sporadic follow-up two-step campaigns

*Implementation*
Use the following implementation:

First permission method: Refers to the opt-in or permission request that is sent to users the very first time they log in. Depending on the strategy you choose, the way you seek the first permission may differ.Use a self-handled opt-in method to trigger notifications requesting push permission directly on every app open. In this approach, the notification prompt is displayed until the user clicks Don’t allow twice.

Follow-up method: Follow-up in-app notifications are sent as a nudge to encourage users to grant push permission or opt-in to receive push notifications from the app. To use this method, you must space out a two-step opt-in campaign regularly with a few days delay between campaigns. You can set up the campaign by adding the push notification to a navigable screen. After the user clicks the notification, you can trigger a single-step opt-in push notification. The follow-up campaign should follow these conditions:

Segmentation: All users
Trigger: Homepage screen
Minimum delay between 2 campaigns: 10 days

Use case-based: This is a trigger-based two-step opt-in campaign. For example, you could set up an in-app campaign that is triggered on certain events such as the “Checkout complete” event, Thank-you screen, Upcoming events screen, and “Subscribed to program”. You can select the event trigger based on the event of your choice and add the segmentation criteria as All users.

For more details, refer to Implementation Details.

*Insights from early data*

We observed that 30-60% of users accept push prompts in the first session with or without a rationale.

This strategy also uses a **self-handled opt-in** and a two-step opt-in campaign but may display the initial prompt less frequently than the aggressive strategy.

*   **Example Use Cases:**
    *   *Gaming app:* Prompting users for notifications when energy is restored or a tournament starts.
    *   *Travel app:* Requesting permission to send notifications about flight delays or gate changes.

### Conservative

*   **Target audience:** Apps where users are sensitive about permissions and require a clear explanation of the value of opting in (e.g., health & fitness apps, finance apps).

Examples

The following is an example of where this strategy can be employed:
User lands on the home page and sees the 2-step opt-in push

*Implementation*
Use the following implementation:

First permission method: Refers to the opt-in or permission request that is sent to users the very first time they log in. Depending on the strategy you choose, the way you seek the first permission may differ.Use a self-handled opt-in method to trigger notifications requesting push permission directly on every app open. In this approach, the notification prompt is displayed until the user clicks Don’t allow twice.

Follow-up method: Follow-up in-app notifications are sent as a nudge to encourage users to grant push permission or opt-in to receive push notifications from the app. To use this method, you must space out a two-step opt-in campaign regularly with a few days delay between campaigns. You can set up the campaign by adding the push notification to a navigable screen. After the user clicks the notification, you can trigger a single-step opt-in push notification. The follow-up campaign should follow these conditions:

Segmentation: All users
Trigger: Homepage screen
Minimum delay between 2 campaigns: 10 days

Use case-based: This is a trigger-based two-step opt-in campaign. For example, you could set up an in-app campaign that is triggered on certain events such as the “Checkout complete” event, Thank-you screen, Upcoming events screen, and “Subscribed to program”. You can select the event trigger based on the event of your choice and add the segmentation criteria as All users.

For more details, refer to Implementation Details.

*Insights from early data*

We observed that 30-60% of users accept push prompts in the first session with or without a rationale.

This strategy focuses on using a **two-step opt-in campaign** to provide context and value before requesting permission. It may also use the **self-handled opt-in**, but with a stronger emphasis on providing a clear rationale beforehand.

*   **Example Use Cases:**
    *   *Health & fitness app:* Explaining how notifications can remind users to exercise or take medication.
    *   *Finance app:* Describing how notifications can alert users to important account activity or investment opportunities.

### Use Case Only

*   **Target audience:** Apps that only use push notifications for specific functional purposes (e.g., ride-sharing apps, food delivery apps).

Examples

The following are some examples of where this strategy can be employed:

The user taps an "alert bell" button.
The user chooses to follow someone's social media account.
The user submits an order for food delivery.

*Implementation*
Use the following implementation:
Use case-based: This is a trigger-based two-step opt-in campaign. For example, you could set up an in-app campaign that is triggered on certain events such as the “Checkout complete” event, Thank-you screen, Upcoming events screen, and “Subscribed to program”. You can select the event trigger based on the event of your choice and add the segmentation criteria as All users.
For more details, refer to Implementation Details.

*Insights from early data*

We observed that this will lead to a low opt-in rate because you’re only reaching out to the user who performs the use case actions.

This strategy *only* uses **use case-based two-step opt-ins**. The app only requests permission when the user takes a specific action that warrants a notification.

*   **Example Use Cases:**
    *   *Ride-sharing app:* Requesting permission to send notifications about driver arrival times and fare updates.
    *   *Food delivery app:* Requesting permission to send notifications about order status and delivery updates.