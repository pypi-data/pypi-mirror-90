# All functions computing a name used across components

def get_account_extract_table_name(
    account_id: str,
    client_id: str,
    account_type: str) -> str:
    return f'{client_id}.{account_type}_extract_{account_id}_campaign'
