# Problem Statement & System Design

## Problem Statement
Small-to-medium warehouse operators often lack simple, lightweight inventory tracking systems. Managing stock without real-time tracking leads to overstocking, stockouts, and delayed order fulfillments.

## Solution
The Warehouse Stock Tracker provides a terminal-based interface designed to allow owners and warehouse personnel to manage stock levels, receive automated low-stock warnings, calculate total inventory valuation, and securely persist inventory data locally in JSON format.

## Objectives
1. **Stock Management:** Enable easy addition, updating, and adjustment of inventory items (SKUs).
2. **Safety Thresholds:** Alert operators immediately when stock drops to or below pre-configured safety stock limits.
3. **Data Integrity:** Prevent invalid entries and ensure thread/session data persistence using structured local storage.
4. **Testability:** Maintain high coverage with modular, testable components.