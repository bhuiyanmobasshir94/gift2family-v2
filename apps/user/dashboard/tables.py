from django.utils.translation import gettext_lazy as _

from django_tables2 import A, Column, LinkColumn, TemplateColumn

from oscar.core.loading import get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')


class UserTable(DashboardTable):
    check = TemplateColumn(
        template_name='oscar/dashboard/users/user_row_checkbox.html',
        verbose_name=' ', orderable=False)
    email = LinkColumn('agents_dashboard:agent-detail', args=[A('id')],
                       accessor='email')
    name = Column(accessor='get_full_name',
                  order_by=('last_name', 'first_name'))
    active = Column(accessor='is_active')
    staff = Column(accessor='is_staff')
    agent = Column(accessor='is_agent')
    date_registered = Column(accessor='date_joined')
    num_orders = Column(accessor='orders.count', orderable=False, verbose_name=_('Number of Orders'))
    actions = TemplateColumn(
        template_name='agents/dashboard/user_row_actions.html',
        verbose_name=' ')

    icon = "group"

    class Meta(DashboardTable.Meta):
        template = 'agents/dashboard/table.html'