# Copyright (C) 2020 - Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def set_stock_warehouse_external_ids(env, company_external_id):
    module, external_id = company_external_id.split(".")
    try:
        company = env.ref(company_external_id, raise_if_not_found=False)
        if not company:
            _logger.warning(f"Company external ID {company_external_id} not found, skipping warehouse setup")
            return
    except ValueError:
        _logger.warning(f"Company external ID {company_external_id} not found, skipping warehouse setup")
        return
        
    warehouse = env["stock.warehouse"].search(
        [("company_id", "=", company.id)], limit=1
    )
    
    if not warehouse:
        _logger.warning(f"No warehouse found for company {company.name} ({company_external_id})")
        return

    data_list = [
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}",
            "record": warehouse,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_loc_stock_id",
            "record": warehouse.lot_stock_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_view_location",
            "record": warehouse.view_location_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_input_location",
            "record": warehouse.wh_input_stock_loc_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_quality_control_location",
            "record": warehouse.wh_qc_stock_loc_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_pack_location",
            "record": warehouse.wh_pack_stock_loc_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_output_location",
            "record": warehouse.wh_pack_stock_loc_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_picking_type_in",
            "record": warehouse.in_type_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_picking_type_internal",
            "record": warehouse.int_type_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_pick_type_internal",
            "record": warehouse.pick_type_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_pack_type_internal",
            "record": warehouse.pack_type_id,
            "noupdate": True,
        },
        {
            "xml_id": f"l10n_br_stock.wh_{external_id}_picking_type_out",
            "record": warehouse.out_type_id,
            "noupdate": True,
        },
    ]
    env["ir.model.data"]._update_xmlids(data_list)


def pre_init_hook(cr):
    """Import XML data to change core data"""

    if not tools.config["without_demo"]:
        _logger.info(_("Loading l10n_br_stock warehouse external ids..."))
        env = api.Environment(cr, SUPERUSER_ID, {})
        try:
            set_stock_warehouse_external_ids(env, "l10n_br_base.empresa_simples_nacional")
            set_stock_warehouse_external_ids(env, "l10n_br_base.empresa_lucro_presumido")
        except Exception as e:
            _logger.warning(f"Failed to set warehouse external ids: {e}")
    else:
        _logger.info(_("Demo data disabled, skipping l10n_br_stock warehouse external ids..."))
