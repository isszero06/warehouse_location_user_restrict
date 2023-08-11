

from odoo import api, fields, models, Command, _



class ResUsers(models.Model):
    _inherit = 'res.users'

    stock_warehouse_ids = fields.Many2many(string='Allwed Stock Warehouses', comodel_name="stock.warehouse", relation="stock_warehouse_id_rel",column1="user_id" , column2="stock_warehouse_id")
    stock_location_ids = fields.Many2many(string='Allwed Stock Locations', comodel_name="stock.location", relation="stock_location_id_rel",column1="user_id" , column2="stock_location_id")
    stock_warehouse_comp_ids = fields.Many2many('stock.warehouse',compute='_compute_warehouse_ids',string='Allowed Warehouses For Current Company')
    stock_location_comp_ids = fields.Many2many('stock.location',compute='_compute_locations_ids',string='Allowed stock locations For Current Company')

    def _compute_warehouse_ids(self):
        if self.stock_warehouse_ids:
            self.stock_warehouse_comp_ids = self.stock_warehouse_ids.filtered(lambda m: m.company_id.id == self.env.company.id).ids
        else:
            self.stock_warehouse_comp_ids = False

    def _compute_locations_ids(self):
        if self.stock_location_ids:
            self.stock_location_comp_ids = self.stock_location_ids.filtered(lambda m: m.company_id.id == self.env.company.id).ids
        else:
            self.stock_location_comp_ids = False

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    def _default_domain_user_ids(self):
        return [('groups_id', 'in', self.env.ref('stock.group_stock_user').id)]


    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Allowed Users",
        relation="stock_warehouse_id_rel",column1="stock_warehouse_id",column2="user_id",domain=lambda self: self._default_domain_user_ids())


class StockLocation(models.Model):
    _inherit = 'stock.location'

    suitable_users = fields.Many2many("res.users",string='Suitable Allowed Users',compute='_suitable_users')

    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Allowed Users",
        relation="stock_location_id_rel", domain="[('id', 'in', suitable_users)]",column1="stock_location_id",column2="user_id")



    @api.depends('warehouse_id')
    def _suitable_users(self):
        for rec in self:
            if self.usage=='internal':
                if rec.warehouse_id.user_ids:
                    rec.suitable_users = rec.warehouse_id.user_ids
                else:
                    rec.suitable_users = False
            else:
                rec.suitable_users = False

    # def write(self, values):
    #     res = super(StockLocation, self).write(values)
    #     if 'user_ids' in values:
    #         picking_type_ids = self.env['stock.picking.type'].with_context(active_test=False).search([('warehouse_id', '=', self.warehouse_id.id),('company_id', '=', self.env.company.id)])
    #         for picking in picking_type_ids:
    #             picking._allowed_users()
    #     return res

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    allowed_users = fields.Many2many("res.users",string='Allowed Users',compute='_allowed_users')



    check_allowed_user = fields.Boolean(compute='_check_allowed_user')



    @api.depends('state')
    def _compute_show_validate(self):
        for picking in self:
            if not (picking.immediate_transfer) and picking.state == 'draft':
                picking.show_validate = False
            elif picking.state not in ('draft', 'waiting', 'confirmed', 'assigned'):
                picking.show_validate = False
            else:
                user = self.env.user
                if picking.allowed_users and user in (picking.allowed_users):
                    picking.show_validate = True
                elif picking.allowed_users and user not in (picking.allowed_users):
                    picking.show_validate = False
                elif not picking.allowed_users:
                    picking.show_validate = True
                else:
                    picking.show_validate = True


    @api.onchange('state')
    def _allowed_users(self):
        for record in self:
            user = self.env.user
            record.allowed_users = False
            if record.picking_type_id.code == 'outgoing' and (record.location_id and record.location_id.user_ids):
                record.allowed_users = record.location_id.user_ids

            elif record.picking_type_id.code == 'internal':
                if record.state not in ('assigned','confirmed') and record.location_id and record.location_id.user_ids: 
                    record.allowed_users = record.location_id.user_ids
                if record.state in ('assigned','confirmed') and record.location_dest_id and record.location_dest_id.user_ids: 
                    record.allowed_users = record.location_dest_id.user_ids

            elif record.picking_type_id.code == 'incoming' and (record.location_dest_id and record.location_dest_id.user_ids):
                record.allowed_users = record.location_dest_id.user_ids
            else:
                record.allowed_users = False



    @api.depends('allowed_users')
    def _check_allowed_user(self):
        for picking in self:
            user = self.env.user
            picking.check_allowed_user = False
            if picking.allowed_users and user in (picking.allowed_users):
                picking.check_allowed_user = True
            elif picking.allowed_users and user not in (picking.allowed_users):
                picking.check_allowed_user = False
            elif not picking.allowed_users:
                picking.check_allowed_user = True

        
   
class StockQuant(models.Model):
    _inherit = 'stock.quant'

class StockScrap(models.Model):
    _inherit = 'stock.scrap'
