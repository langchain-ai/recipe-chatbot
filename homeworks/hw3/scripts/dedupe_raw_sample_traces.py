#!/usr/bin/env python3
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any

def load_and_dedupe_traces(csv_path: str) -> List[Dict[str, Any]]:
    """Load traces from CSV and dedupe them."""
    print(f"Loading traces from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Total traces loaded: {len(df)}")
    
    # Dedupe based on query + dietary_restriction + trace_id combination
    # Using query content as the main deduplication key since traces should be unique per query
    df_deduped = df.drop_duplicates(subset=['query', 'dietary_restriction', 'trace_id'])
    
    print(f"Traces after deduplication: {len(df_deduped)}")
    
    return df_deduped.to_dict('records')

def sample_traces(traces: List[Dict[str, Any]], n_success: int = 10, n_failure: int = 10) -> List[Dict[str, Any]]:
    """Sample n_success PASS traces and n_failure FAIL traces."""
    df = pd.DataFrame(traces)
    
    # Check what label values we have
    print("Available label values:", df['label'].unique())
    
    success_traces = df[df['label'] == 'PASS']
    failure_traces = df[df['label'] == 'FAIL']
    
    print(f"Available success traces: {len(success_traces)}")
    print(f"Available failure traces: {len(failure_traces)}")
    
    # Sample the requested number (or all available if less than requested)
    sampled_success = success_traces.sample(n=min(n_success, len(success_traces)), random_state=42)
    sampled_failure = failure_traces.sample(n=min(n_failure, len(failure_traces)), random_state=42)
    
    # Combine and shuffle
    sampled_df = pd.concat([sampled_success, sampled_failure]).sample(frac=1, random_state=42)
    
    return sampled_df.to_dict('records')

def main():
    # Set up paths
    script_dir = Path(__file__).parent
    hw3_dir = script_dir.parent
    data_dir = hw3_dir / "data"
    traces_path = data_dir / "labeled_traces.csv"
    
    if not traces_path.exists():
        print(f"Error: {traces_path} not found!")
        return
    
    # Load and dedupe traces
    traces = load_and_dedupe_traces(str(traces_path))
    
    # Sample 10 success and 10 failure traces
    sampled_traces = sample_traces(traces, n_success=10, n_failure=10)
    
    print(f"\nFinal sample contains {len(sampled_traces)} traces")
    
    # Display summary
    df_sample = pd.DataFrame(sampled_traces)
    pass_count = len(df_sample[df_sample['label'] == 'PASS'])
    fail_count = len(df_sample[df_sample['label'] == 'FAIL'])
    
    print(f"PASS traces: {pass_count}")
    print(f"FAIL traces: {fail_count}")
    
    # Display the sampled traces
    print(f"\n{'='*80}")
    print("SAMPLED TRACES:")
    print(f"{'='*80}")
    
    for i, trace in enumerate(sampled_traces, 1):
        print(f"\n--- Trace {i} (Label: {trace['label']}) ---")
        print(f"Query: {trace['query'][:100]}...")
        print(f"Dietary Restriction: {trace['dietary_restriction']}")
        print(f"Trace ID: {trace['trace_id']}")
        if trace.get('error'):
            print(f"Error: {trace['error']}")
    
    # Save to CSV file
    output_path = data_dir / "sampled_labeled_traces.csv"
    df_sample = pd.DataFrame(sampled_traces)
    df_sample.to_csv(output_path, index=False)
    print(f"\nSaved sampled traces to: {output_path}")
    
    return sampled_traces

if __name__ == "__main__":
    sampled_traces = main()