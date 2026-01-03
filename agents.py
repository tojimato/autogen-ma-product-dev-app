"""Agent definitions for the product development engine."""

import logging
from typing import Dict, Any
from autogen import ConversableAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductDefinerAgent(ConversableAgent):
    """Agent responsible for defining what the product/service offers and to whom."""

    def __init__(self, llm_config: Dict[str, Any], functions: list = None, temperature: float = 0.2):
        description = (
            "Answers questions about product definition, market analysis, customer segmentation, "
            "target markets, value proposition, and problem-solution fit. "
            "Call on this agent when you need to establish what the product is, who it serves, "
            "and what makes it uniquely valuable in the market."
        )
        system_message = (
            "You are the Product Definer - an expert in market analysis, customer discovery, "
            "and product positioning.\n\n"
            "Your responsibilities:\n"
            "1. Define the core product or service offering with clarity and precision.\n"
            "2. Identify and characterize target customers, market segments, and buyer personas.\n"
            "3. Articulate the unique value proposition and competitive advantages.\n"
            "4. Consider market gaps, customer pain points, and solution fit.\n\n"
            "Provide your analysis in 2-3 well-structured sentences. Focus on being specific, "
            "actionable, and grounded in market reality."
        )
        # Update llm_config with temperature
        config = dict(llm_config) if isinstance(llm_config, dict) else llm_config
        if isinstance(config, dict):
            config["temperature"] = temperature
        super().__init__(
            name="ProductDefiner",
            system_message=system_message,
            description=description,
            llm_config=config,
            functions=functions or [],
            human_input_mode="NEVER",
        )

class ValueCreatorAgent(ConversableAgent):
    """Agent responsible for how the product creates value from start to end for customers."""

    def __init__(self, llm_config: Dict[str, Any], functions: list = None, temperature: float = 0.4):
        description = (
            "Answers questions about customer journey mapping, value delivery mechanisms, "
            "customer experience design, value chain analysis, and operational workflows. "
            "Call on this agent when you need to explain how value flows to customers from "
            "initial engagement through to outcomes and retention."
        )
        system_message = (
            "You are the Value Creator - an expert in customer journey mapping, experience "
            "design, and operational excellence.\n\n"
            "Your responsibilities:\n"
            "1. Map the complete customer journey from awareness to post-purchase outcomes.\n"
            "2. Explain how the product delivers tangible value at each stage of engagement.\n"
            "3. Describe the operational processes, workflows, and touchpoints that enable "
            "value delivery.\n"
            "4. Consider user experience, efficiency, and sustainability of value creation.\n\n"
            "Provide your analysis in 2-3 well-structured sentences. Focus on concrete mechanisms "
            "and customer outcomes."
        )
        # Update llm_config with temperature
        config = dict(llm_config) if isinstance(llm_config, dict) else llm_config
        if isinstance(config, dict):
            config["temperature"] = temperature
        super().__init__(
            name="ValueCreator",
            system_message=system_message,
            description=description,
            llm_config=config,
            functions=functions or [],
            human_input_mode="NEVER",
        )

class PricingStrategistAgent(ConversableAgent):
    """Agent responsible for pricing strategy."""

    def __init__(self, llm_config: Dict[str, Any], functions: list = None, temperature: float = 0.3):
        description = (
            "Answers questions about pricing models, pricing strategy, revenue optimization, "
            "market positioning, cost analysis, and financial viability. "
            "Call on this agent when you need to develop a pricing strategy that aligns with "
            "market positioning, customer segments, and business goals."
        )
        system_message = (
            "You are the Pricing Strategist - an expert in pricing models, market positioning, "
            "and revenue optimization.\n\n"
            "Your responsibilities:\n"
            "1. Develop a clear, defensible pricing strategy grounded in value delivered.\n"
            "2. Consider market dynamics, competitor positioning, and customer willingness to pay.\n"
            "3. Evaluate different pricing models (subscription, one-time fee, tiered, freemium, etc.) "
            "and recommend the best fit.\n"
            "4. Factor in cost structure, margin targets, and scalability.\n\n"
            "Provide your strategy in 2-3 well-structured sentences. Include specific price points "
            "or models and your reasoning."
        )
        # Update llm_config with temperature
        config = dict(llm_config) if isinstance(llm_config, dict) else llm_config
        if isinstance(config, dict):
            config["temperature"] = temperature
        super().__init__(
            name="PricingStrategist",
            system_message=system_message,
            description=description,
            llm_config=config,
            functions=functions or [],
            human_input_mode="NEVER",
        )

class MarketingSalesAgent(ConversableAgent):
    """Agent responsible for marketing and sales processes."""

    def __init__(self, llm_config: Dict[str, Any], functions: list = None, temperature: float = 0.6):
        description = (
            "Answers questions about go-to-market strategy, customer acquisition, sales funnels, "
            "marketing channels, customer retention, and launch planning. "
            "Call on this agent when you need to create a comprehensive marketing and sales "
            "strategy for product launch and customer acquisition."
        )
        system_message = (
            "You are the Marketing & Sales Strategist - an expert in go-to-market strategy, "
            "customer acquisition, and revenue growth.\n\n"
            "Your responsibilities:\n"
            "1. Define the go-to-market strategy including target channels and customer segments.\n"
            "2. Design the sales funnel with clear stages: awareness, consideration, conversion, "
            "and retention.\n"
            "3. Outline key marketing campaigns, messaging, and promotional activities.\n"
            "4. Consider sales processes, key partnerships, and success metrics.\n\n"
            "Provide your strategy in 2-3 well-structured sentences. Be specific about channels, "
            "tactics, and expected outcomes."
        )
        # Update llm_config with temperature
        config = dict(llm_config) if isinstance(llm_config, dict) else llm_config
        if isinstance(config, dict):
            config["temperature"] = temperature
        super().__init__(
            name="MarketingSales",
            system_message=system_message,
            description=description,
            llm_config=config,
            functions=functions or [],
            human_input_mode="NEVER",            
        )


class OrchestratorAgent(ConversableAgent):
    """Master controller that manages the workflow and coordinates specialist agents."""

    def __init__(self, llm_config: Dict[str, Any], functions: list = None, temperature: float = 0.3):
        description = (
            "Coordinates the product development workflow among specialist team members. "
            "Manages ProductDefiner, ValueCreator, PricingStrategist, and MarketingSales to ensure "
            "all required outputs are collected. Decides workflow progression based on completion status."
        )
        system_message = (
            "You are the Orchestrator - the master coordinator for the product development team.\n\n"
            "Your role is to coordinate with each specialist to complete the product development process:\n"
            "- ProductDefiner: Develops the product definition\n"
            "- ValueCreator: Explains value delivery\n"
            "- PricingStrategist: Develops pricing strategy\n"
            "- MarketingSales: Creates go-to-market strategy\n\n"
            "Guide the team through their work. Request specialists by name when needed. "
            "Once all four have completed their outputs, ask the user if revisions are needed. "
            "If yes, coordinate revisions. If no, conclude the session.\n\n"
            "Track which specialists have completed and request outputs from those who haven't. "
            "Keep responses focused and maintain the conversation flow."
        )
        # Update llm_config with temperature
        config = dict(llm_config) if isinstance(llm_config, dict) else llm_config
        if isinstance(config, dict):
            config["temperature"] = temperature
        super().__init__(
            name="Orchestrator",
            system_message=system_message,
            description=description,
            llm_config=config,
            functions=functions or [],
            human_input_mode="NEVER",
        )

