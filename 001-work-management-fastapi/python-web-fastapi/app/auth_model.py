"""Generated authentication bindings; no business resource or ownership contract."""
from Q import Q
from teaql.runtime import ContextEntityRef

ALLOW_SELF_REGISTRATION = True

def bind_context(context, actor=None):
    context.with_active_root(ContextEntityRef("WorkSpace", 1))
    context.set_user_identifier(str(actor) if actor is not None else "example-auth")
    return context


async def load_root(context):
    return await (Q.work_spaces().with_id_is(1)
                  .comment("Find the generated workspace")
                  .purpose("Attach a new record to its workspace").execute_for_one(context))


async def account_by_id(context, account_id):
    return await (Q.work_accounts().whose_id_is(account_id)
                  .comment("Load the signed-in account by ID")
                  .purpose("Resolve the session actor").execute_for_one(context))


async def account_by_email(context, address):
    return await (Q.work_accounts().whose_email_address_is(address).limit(1)
                  .comment("Find the account for a normalized email")
                  .purpose("Register or authenticate an account").execute_for_one(context))


def credential(account):
    return account.passwordHash


async def create_account(context, name, address, password_hash):
    user = (Q.work_accounts().comment("Initialize a new account")
            .purpose("Register a workspace member").new_entity(context))
    user.update_work_space(await load_root(context))
    user.update_display_name(name)
    user.update_email_address(address)
    user.update_password_hash(password_hash)
    await user.audit_as("Register a workspace member").save(context)
    return user
