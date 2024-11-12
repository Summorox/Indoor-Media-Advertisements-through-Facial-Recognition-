# Indoormedia
## Overview
This repository contains a group project developed as part of a master's program in Artificial Intelligence at ISEP, completed in 2023. It is a prototype for a multi-agent system designed for targeted advertising. The system uses motion detection and facial recognition to identify the demographics of passersby, enabling the display of ads tailored to these characteristics. An auction-based algorithm selects the ad to display based on relevance and potential impact.

This project includes diagrams illustrating the overall system flow and agent interactions.

## System Agents
1. **Motion Detection Agent**: Uses an ESP32 device to detect the presence of a person in front of the display. When motion is detected, it sends a trigger signal to the core agent to initiate demographic analysis.
2. **Facial Recognition Agent**: Uses OpenCV to perform real-time facial recognition, extracting demographic features like age and gender.  
3.  **Core Agent**: The central coordinator of the system, sending and receiving data between the agents.
4. **Auction Agent**: Coordinates the auction for ad selection. Upon receiving demographic data from the core agent, the auction agent collects bids from each auction participant agent and determines the highest-bid ad relevant to the demographic profile.
5. **Auction Participant Agents**: Represent different advertisers or ad categories. Each participant agent submits a bid to the auction agent based on the demographic data. 
6. **Display Agent**: Retrieves the selected ad from a local folder (serving as a mock database) based on the auction results and displays it on the screen.
