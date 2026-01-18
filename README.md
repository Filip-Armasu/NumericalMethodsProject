Multi-Agent Market Simulation

This project implements a multi-agent market simulation in Python using the Mesa framework. The model simulates firms and consumers interacting in a market and visualizes how market shares evolve over time, including the emergence of dominant firms.


Model Description

Agents: 

1. Firms
-Set prices
-Produce goods at a cost
-Earn revenue from consumers
-Accumulate profits and losses
-Can be penalized after repeated losses (shareholder penalty)

2. Consumers
-Have a budget
-Choose among affordable firms
-Purchase goods each simulation step

Market Dynamics:
-Firms compete for consumers
-Market shares are calculated using cumulative revenue
-Prices adjust based on sales and capital
-Repeated losses trigger a shareholder penalty instead of immediate firm exit
-Firms exit once they run out of capital


How to Run
1. Activate the virtual environment
python3 -m venv venv
venv\Scripts\Activate

In case of errors use this before activating venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

2. Install dependencies
python -m pip install -r requirements.txt

3. Run the simulation with either:
python main.py for the final step of the simulation  
python animation.py for the animated market share evolution


In main.py or the animation.py, you can adjust:
-Number of firms
-Number of consumers
-Fixed production costs
-Income per step
-Shareholder penalty and Investor bonus
-Loss streak threshold and Win streak threshold
-Brand Gain, Decay and Weight
-Start Boost


Contribution Statement:
Armasu Filip - Visualization, Animation
Paval-Danila Amalia - Model Design, Python Implementation 
Both - Mathematical Formulation, Debugging, Analysis, Parameter Experimentation

Video with samples: https://www.youtube.com/watch?v=mOEa9dZ4ilA