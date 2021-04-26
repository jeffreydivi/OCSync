# OCSync
*A simple data aggregator and control panel for Minecraft*

## The Problem
You are playing on a Minecraft server. You have [nuclear power generation](https://tenyx.de/brgc/), [items you want to keep eye on](https://refinedmods.com/refined-storage/wiki/opencomputers-api.html), and [trains you want to automate](https://github.com/TeamOpenIndustry/ImmersiveRailroading/wiki/Open-Computers).

Now, what if you can watch all of these, in one place, on any device? **That is the goal of OCSync.**

## The Implementation

To do this, we need three things:
- OpenComputers installed on a Minecraft server with Internet card support
- A (here, it will be browser-based) interface to make data aggregation and control easy
- A server that connects the two.

For endpoint communication, I feel that WebSockets is best; it allows for events to instantaneously be transmitted between client and server without spamming either with little delay.

As for each component, each will be developed as separate code-bases that can talk to each other seamlessly with WebSockets.

## Considerations

- **Security.** We don't want someone to be able to arbitrarily edit or access data, which would break data integrity and confidentiality.
- **Performance.** While performance may not be a huge concern on the server-side, it is key on the Minecraft side. Don't send data unless needed, and cache when possible.
- **Reliability.** We want this to work. No finagling when something sour happens. It should be set-and-forget. We also want it to be resilliant to potential abuse, further ensuring data and network avaiablity.
- **Flexibility.** What if we want to add or remove components? What if we decide, on a whim, to add or remove a data source? We shouldn't have to re-design anything to make that happen.
