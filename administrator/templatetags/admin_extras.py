from django import template


def status_label(value):
    """
    Displays labels for each seller status
    """
    status_map = {
        'pending': '<span class="label label-warning">Pending</span>',
        'approved': '<span class="label label-success">Approved</span>',
        'rejected': '<span class="label label-important">Rejected</span>',
        'signedup': '<span class="label label-info">Signed Up</span>',
        }
    return status_map[value]

register = template.Library()
register.filter('status_label', status_label)
