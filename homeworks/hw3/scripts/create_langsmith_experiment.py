#!/usr/bin/env python3
import pandas as pd
from typing import List, Dict, Any
from langsmith import Client
from pathlib import Path
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()

console = Console()

def load_traces(csv_path: str) -> List[Dict[str, Any]]:
    """Load traces from CSV file."""
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

def main():
    """Main function to label traces."""
    console.print("[bold blue]Recipe Bot Trace Labeling")
    console.print("=" * 50)
    
    # Set up paths
    script_dir = Path(__file__).parent
    hw3_dir = script_dir.parent
    data_dir = hw3_dir / "data"
    
    # Load raw traces
    traces_path = data_dir / "sampled_labeled_traces.csv"
    if not traces_path.exists():
        console.print(f"[red]Error: {traces_path} not found!")
        console.print("[yellow]Please checkout this repo again.")
        return
    
    traces = load_traces(str(traces_path))
    print(traces[0])
    
    console.print(f"[green]Loaded {len(traces)} traces")
    
    dataset_name = "Recipe Bot Dietary Adherence"

    client = Client()

    examples = [{
        "inputs": {
            "query": trace["query"],
            "dietary_restriction": trace["dietary_restriction"],
            "response_index": i,
        },
    } for i, trace in enumerate(traces)]

    dataset = client.create_dataset(dataset_name)
    client.create_examples(dataset_id=dataset.id, examples=examples)
    
    def target(inputs: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        trace = traces[inputs["response_index"]]
        return {"response": trace["response"]}

    res = client.evaluate(
        target,
        data=dataset.id,
    )
    console.print(f"[green]Evaluated {len(res)} traces")

if __name__ == "__main__":
    main()
