from typing import Optional

from invoke import Collection, Context, task


CONFIG = {
    "terraform": {
        "organisation": None,
        "workspace": None,
        "token": None,
    }
}


# Terraform deployment workflow


@task
def update(ctx, variable="", value="", organisation=None, workspace=None, token=None):
    """Update variable in Terraform cloud."""
    cmd = f"noostf update --variable {variable} --value '{value}'"
    ctx.run(cmd + _append_credentials(ctx, organisation, workspace, token), pty=True)


@task
def run(ctx, message="", organisation=None, workspace=None, token=None):
    """Run a plan in Terraform cloud."""
    cmd = f"noostf run --message '{message}'"
    ctx.run(cmd + _append_credentials(ctx, organisation, workspace, token), pty=True)


def _append_credentials(
    ctx: Context, organisation: Optional[str], workspace: Optional[str], token: Optional[str]
) -> str:
    cmd = ""
    for arg in ctx.terraform:
        # Check credentials
        secret = locals()[arg] or ctx.terraform[arg]
        assert secret is not None, f"Missing Terraform Cloud {arg}."
        # Return credentials args
        cmd += f" --{arg} {secret}"
    return cmd


ns = Collection("terraform")
ns.configure(CONFIG)
ns.add_task(update)
ns.add_task(run)
