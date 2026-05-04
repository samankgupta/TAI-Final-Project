"""Command-line interface."""

import sys
import click
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from evaluation.experiment_runner import ExperimentRunner
from evaluation.compare_stages import StageComparator
from config import OUTPUT_DIR


@click.group()
def cli():
    """Resume Trust Lab System"""
    pass


def _parse_request_file(request_file: str):
    """Parse role/job description from a json or text file."""
    path = Path(request_file)
    if not path.exists():
        raise FileNotFoundError(f"Request file not found: {request_file}")

    if path.suffix.lower() == '.json':
        data = json.loads(path.read_text())
        role = data.get('role')
        job_description = data.get('job_description') or data.get('jobDescription')
        top_n = int(data.get('top_n', data.get('topN', 5)))
        if not role or not job_description:
            raise ValueError("JSON file must contain 'role' and 'job_description'")
        return role, job_description, top_n

    # Text format:
    # role: E-commerce Specialist
    # top_n: 5
    # job_description: <text or multiline>
    content = path.read_text()
    lines = content.splitlines()
    role = None
    top_n = 5
    job_description = []
    in_job_desc = False

    for raw_line in lines:
        line = raw_line.strip()
        lower = line.lower()
        if lower.startswith('role:'):
            role = line.split(':', 1)[1].strip()
            continue
        if lower.startswith('top_n:'):
            top_n = int(line.split(':', 1)[1].strip())
            continue
        if lower.startswith('job_description:'):
            in_job_desc = True
            job_description.append(line.split(':', 1)[1].strip())
            continue
        if in_job_desc:
            job_description.append(raw_line)

    jd_text = '\n'.join([x for x in job_description if x.strip()]).strip()
    if not role or not jd_text:
        raise ValueError("Text file must include 'role:' and 'job_description:'")
    return role, jd_text, top_n


def _build_reasoning(row, until_stage: int) -> str:
    """Create a human-readable selection reason."""
    if until_stage == 5:
        return (
            f"Stage 5 score={row.get('improved_score', 'NA')}, "
            f"hallucination_rate={row.get('hallucination_rate', 0):.2f}. "
            f"LLM rationale: {row.get('improved_reasoning', '')}"
        )
    if until_stage == 4:
        return (
            f"Stage 4 Gemini score={row.get('gemini_score', 'NA')}. "
            f"LLM rationale: {row.get('gemini_reasoning', '')}"
        )
    if until_stage == 3:
        baseline = row.get('baseline_score', 'NA')
        emb = row.get('embedding_score', 'NA')
        return f"Stage 3 semantic match score={emb}, baseline keyword score={baseline}."
    return "Selected based on ranking score."


def _print_final_selection(selected_df, until_stage: int):
    """Print full selected resume details and reasoning."""
    click.echo("\n" + "=" * 70)
    click.echo(f"FINAL SELECTED RESUMES (UP TO STAGE {until_stage})")
    click.echo("=" * 70)

    for idx, (_, row) in enumerate(selected_df.iterrows(), start=1):
        click.echo(f"\n#{idx}")
        click.echo("-" * 70)
        click.echo(f"Role: {row.get('Role', '')}")
        click.echo(f"Selection Reason (system): {_build_reasoning(row, until_stage)}")
        click.echo("Resume Details:")
        click.echo(str(row.get('Resume', '')))


@cli.command()
@click.option('--stage', type=int, required=True)
@click.option('--role', type=str, default="E-commerce Specialist")
@click.option('--sample-size', type=int, default=None)
def run_stage(stage, role, sample_size):
    """Run a specific stage."""
    runner = ExperimentRunner(sample_size=sample_size)
    
    if stage == 1:
        runner.run_stage_1(role)
    elif stage == 2:
        if runner.df is None:
            runner.run_stage_1(role)
        runner.load_job_description()
        runner.run_stage_2()
    elif stage == 3:
        if runner.df is None:
            runner.run_stage_1(role)
        runner.load_job_description()
        runner.run_stage_3()
    elif stage == 4:
        if runner.df is None:
            runner.run_stage_1(role)
        runner.load_job_description()
        runner.run_stage_4()
    elif stage == 5:
        if runner.df is None:
            runner.run_stage_1(role)
        runner.load_job_description()
        runner.run_stage_5()


@cli.command()
@click.option('--role', type=str, default="E-commerce Specialist")
@click.option('--sample-size', type=int, default=1000)
def run_all(role, sample_size):
    """Run all stages."""
    runner = ExperimentRunner(sample_size=sample_size)
    runner.run_all(role)
    runner.compute_metrics()


@cli.command()
@click.option('--stage1', type=int, required=True)
@click.option('--stage2', type=int, required=True)
def compare(stage1, stage2):
    """Compare two stages."""
    comparison = StageComparator.compare_rankings(stage1, stage2)
    click.echo(f"\nComparison: {comparison['stage_a']} vs {comparison['stage_b']}")
    click.echo(f"TSS: {comparison['tss_top_k']:.3f}")
    click.echo(f"Overlap: {comparison['overlap']}")


@cli.command()
def status():
    """Show experiment status."""
    output_files = list(OUTPUT_DIR.glob("stage_*.json"))
    
    if not output_files:
        click.echo("No stages completed")
        return
    
    import json
    for f in sorted(output_files):
        with open(f) as fp:
            data = json.load(fp)
        click.echo(f"Stage {data['stage']}: {data['output_count']} outputs")


@cli.command('run-pipeline')
@click.option('--request-file', type=str, required=True, help='Path to txt/json containing role and job_description')
@click.option('--until-stage', type=click.Choice(['3', '4', '5']), default='5', show_default=True)
@click.option('--sample-size', type=int, default=None, help='Optional dataset row limit for faster runs')
@click.option('--max-role-matches', type=int, default=100, show_default=True, help='Maximum role-matching resumes to keep after stage 1')
@click.option('--top-n', type=int, default=None, help='Final number of resumes to print/save')
def run_pipeline(request_file, until_stage, sample_size, max_role_matches, top_n):
    """Run pipeline until stage 3/4/5 and print final top-N resume details with reasoning."""
    role, job_description, file_top_n = _parse_request_file(request_file)
    final_top_n = top_n if top_n is not None else file_top_n
    until = int(until_stage)

    runner = ExperimentRunner(sample_size=sample_size)
    runner.run_stage_1(role, max_role_matches=max_role_matches)
    runner.job_description = job_description
    runner.run_stage_2()
    runner.run_stage_3()
    if until >= 4:
        runner.run_stage_4()
    if until >= 5:
        runner.run_stage_5()

    final_key = f'stage_{until}'
    final_df = runner.ranked_dfs.get(final_key)
    if final_df is None or final_df.empty:
        click.echo('No final results found for selected stage')
        return

    selected_df = final_df.head(final_top_n).copy()
    _print_final_selection(selected_df, until)

    output = {
        'role': role,
        'until_stage': until,
        'top_n': int(final_top_n),
        'selected_resumes': [],
    }

    for rank, (_, row) in enumerate(selected_df.iterrows(), start=1):
        output['selected_resumes'].append({
            'rank': rank,
            'role': row.get('Role', ''),
            'system_reasoning': _build_reasoning(row, until),
            'resume': row.get('Resume', ''),
            'scores': {
                'baseline_score': row.get('baseline_score'),
                'embedding_score': row.get('embedding_score'),
                'gemini_score': row.get('gemini_score'),
                'improved_score': row.get('improved_score'),
                'hallucination_rate': row.get('hallucination_rate'),
            },
        })

    out_file = OUTPUT_DIR / f'final_selection_stage_{until}.json'
    with open(out_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    click.echo(f"\nSaved final selection to {out_file}")


@cli.command('run-stage3')
@click.option('--request-file', type=str, required=True, help='Path to txt/json containing role and job_description')
@click.option('--sample-size', type=int, default=None, help='Optional dataset row limit for faster runs')
@click.option('--max-role-matches', type=int, default=100, show_default=True, help='Maximum role-matching resumes to keep after stage 1')
@click.option('--top-n', type=int, default=5, show_default=True, help='Final number of resumes to print/save')
def run_stage3(request_file, sample_size, max_role_matches, top_n):
    """Run pipeline through stage 3."""
    ctx = click.get_current_context()
    ctx.invoke(run_pipeline, request_file=request_file, until_stage='3', sample_size=sample_size, max_role_matches=max_role_matches, top_n=top_n)


@cli.command('run-stage4')
@click.option('--request-file', type=str, required=True, help='Path to txt/json containing role and job_description')
@click.option('--sample-size', type=int, default=None, help='Optional dataset row limit for faster runs')
@click.option('--max-role-matches', type=int, default=100, show_default=True, help='Maximum role-matching resumes to keep after stage 1')
@click.option('--top-n', type=int, default=5, show_default=True, help='Final number of resumes to print/save')
def run_stage4(request_file, sample_size, max_role_matches, top_n):
    """Run pipeline through stage 4."""
    ctx = click.get_current_context()
    ctx.invoke(run_pipeline, request_file=request_file, until_stage='4', sample_size=sample_size, max_role_matches=max_role_matches, top_n=top_n)


@cli.command('run-stage5')
@click.option('--request-file', type=str, required=True, help='Path to txt/json containing role and job_description')
@click.option('--sample-size', type=int, default=None, help='Optional dataset row limit for faster runs')
@click.option('--max-role-matches', type=int, default=100, show_default=True, help='Maximum role-matching resumes to keep after stage 1')
@click.option('--top-n', type=int, default=5, show_default=True, help='Final number of resumes to print/save')
def run_stage5(request_file, sample_size, max_role_matches, top_n):
    """Run pipeline through stage 5."""
    ctx = click.get_current_context()
    ctx.invoke(run_pipeline, request_file=request_file, until_stage='5', sample_size=sample_size, max_role_matches=max_role_matches, top_n=top_n)


if __name__ == '__main__':
    cli()
