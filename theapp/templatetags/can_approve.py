from django import template
register = template.Library()


@register.simple_tag()
def can_approve(user, approval):
    """
    Simply a wrapper for
    checking if user can mark approval
    as approved.
    """

    return approval.can_be_approved_by(user)
