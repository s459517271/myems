-- NOTE: this script is DANGEROUS and may cause data loss so it is for advanced users only
-- 注意: 这个脚本很危险，可能会造成数据丢失，仅限高级用户使用
-- NOTE: before running this script, you should stop the myems-normalization service and myems-aggregation service
-- 注意：运行这个脚本前必须停止myems-normalization服务和myems-aggregation服务
-- NOTE: after running this script, you should start the myems-normalization service and myems-aggregation service
-- 注意：运行这个脚本后必须启动myems-normalization服务和myems-aggregation服务
-- NOTE: the start datetime in database are in UTC
-- 注意：数据库中的开始时间是UTC时间

DELETE FROM `myems_energy_db`.`tbl_combined_equipment_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_combined_equipment_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_combined_equipment_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_container_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_container_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_container_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_container_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_container_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_power_station_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_power_station_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_power_station_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_power_station_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_energy_storage_power_station_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_equipment_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_equipment_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_equipment_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_evcharger_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_microgrid_photovoltaic_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';

-- NOTE: if you delete tbl_offline_meter_hourly, the offline meter files should be reuploaded
-- 注意: 如果删除tbl_offline_meter_hourly数据，离线表文件必须重新上传
-- DELETE FROM `myems_energy_db`.`tbl_offline_meter_hourly`
-- WHERE start_datetime_utc >= '2023-12-31 16:00:00';

DELETE FROM `myems_energy_db`.`tbl_photovoltaic_power_station_generation_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_photovoltaic_power_station_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_photovoltaic_power_station_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_photovoltaic_power_station_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_shopfloor_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_shopfloor_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_space_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_space_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_space_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_store_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_store_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_tenant_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_tenant_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_energy_db`.`tbl_virtual_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';

DELETE FROM `myems_billing_db`.`tbl_combined_equipment_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_combined_equipment_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_combined_equipment_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_container_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_container_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_container_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_container_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_container_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_power_station_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_power_station_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_power_station_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_power_station_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_energy_storage_power_station_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_equipment_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_equipment_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_equipment_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_evcharger_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_microgrid_photovoltaic_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_offline_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_photovoltaic_power_station_generation_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_photovoltaic_power_station_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_photovoltaic_power_station_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_photovoltaic_power_station_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_shopfloor_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_shopfloor_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_space_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_space_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_space_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_store_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_store_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_tenant_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_tenant_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_billing_db`.`tbl_virtual_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';

DELETE FROM `myems_carbon_db`.`tbl_combined_equipment_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_combined_equipment_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_combined_equipment_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_container_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_container_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_container_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_container_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_container_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_power_station_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_power_station_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_power_station_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_power_station_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_energy_storage_power_station_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_equipment_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_equipment_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_equipment_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_charge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_discharge_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_evcharger_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_microgrid_photovoltaic_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_offline_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_photovoltaic_power_station_generation_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_photovoltaic_power_station_grid_buy_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_photovoltaic_power_station_grid_sell_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_photovoltaic_power_station_load_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_shopfloor_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_shopfloor_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_space_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_space_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_space_output_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_store_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_store_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_tenant_input_category_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_tenant_input_item_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
DELETE FROM `myems_carbon_db`.`tbl_virtual_meter_hourly`
WHERE start_datetime_utc >= '2023-12-31 16:00:00';
