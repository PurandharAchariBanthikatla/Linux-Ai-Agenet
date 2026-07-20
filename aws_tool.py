"""
AWS tool: Wrappers for common AWS CLI operations
"""

from tools.shell import run


def list_ec2(region: str = "ap-south-1") -> str:
    out, err, _ = run(
        f"aws ec2 describe-instances --region {region} "
        "--query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress]' "
        "--output table"
    )
    return out or err


def s3_list(bucket: str = "") -> str:
    if bucket:
        out, err, _ = run(f"aws s3 ls s3://{bucket}")
    else:
        out, err, _ = run("aws s3 ls")
    return out or err


def s3_sync(source: str, dest: str) -> str:
    out, err, _ = run(f"aws s3 sync {source} {dest}")
    return out or err


def cloudwatch_logs(group: str, stream: str = "", limit: int = 20) -> str:
    cmd = f"aws logs get-log-events --log-group-name {group} --limit {limit}"
    if stream:
        cmd += f" --log-stream-name {stream}"
    out, err, _ = run(cmd)
    return out or err


def ecr_list(region: str = "ap-south-1") -> str:
    out, err, _ = run(
        f"aws ecr describe-repositories --region {region} --output table"
    )
    return out or err


def iam_whoami() -> str:
    out, err, _ = run("aws sts get-caller-identity")
    return out or err
