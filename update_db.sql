BEGIN;
--
-- Alter field sensor on circpump
--
SET CONSTRAINTS "hotwater_circpump_sensor_id_7e5cfa9f_fk_devices_tempsensor_name" IMMEDIATE; ALTER TABLE "hotwater_circpump" DROP CONSTRAINT "hotwater_circpump_sensor_id_7e5cfa9f_fk_devices_tempsensor_name";
ALTER TABLE "hotwater_circpump" DROP CONSTRAINT "hotwater_circpump_sensor_id_key";
CREATE INDEX "hotwater_circpump_sensor_id_7e5cfa9f" ON "hotwater_circpump" ("sensor_id");
ALTER TABLE "hotwater_circpump" ADD CONSTRAINT "hotwater_circpump_sensor_id_7e5cfa9f_fk_devices_tempsensor_name" FOREIGN KEY ("sensor_id") REFERENCES "devices_tempsensor" ("name") DEFERRABLE INITIALLY DEFERRED;
--
-- Alter field sensor_burn on waterheater
--
SET CONSTRAINTS "hotwater_waterheater_sensor_burn_id_e9390e60_fk_devices_t" IMMEDIATE; ALTER TABLE "hotwater_waterheater" DROP CONSTRAINT "hotwater_waterheater_sensor_burn_id_e9390e60_fk_devices_t";
ALTER TABLE "hotwater_waterheater" DROP CONSTRAINT "hotwater_waterheater_sensor_burn_id_key";
CREATE INDEX "hotwater_waterheater_sensor_burn_id_e9390e60" ON "hotwater_waterheater" ("sensor_burn_id");
ALTER TABLE "hotwater_waterheater" ADD CONSTRAINT "hotwater_waterheater_sensor_burn_id_e9390e60_fk_devices_t" FOREIGN KEY ("sensor_burn_id") REFERENCES "devices_tempsensor" ("name") DEFERRABLE INITIALLY DEFERRED;
--
-- Alter field sensor_in on waterheater
--
SET CONSTRAINTS "hotwater_waterheater_sensor_in_id_58515e97_fk_devices_t" IMMEDIATE; ALTER TABLE "hotwater_waterheater" DROP CONSTRAINT "hotwater_waterheater_sensor_in_id_58515e97_fk_devices_t";
ALTER TABLE "hotwater_waterheater" DROP CONSTRAINT "hotwater_waterheater_sensor_in_id_key";
CREATE INDEX "hotwater_waterheater_sensor_in_id_58515e97" ON "hotwater_waterheater" ("sensor_in_id");
ALTER TABLE "hotwater_waterheater" ADD CONSTRAINT "hotwater_waterheater_sensor_in_id_58515e97_fk_devices_t" FOREIGN KEY ("sensor_in_id") REFERENCES "devices_tempsensor" ("name") DEFERRABLE INITIALLY DEFERRED;
--
-- Alter field sensor_out on waterheater
--
SET CONSTRAINTS "hotwater_waterheater_sensor_out_id_ce02c7c8_fk_devices_t" IMMEDIATE; ALTER TABLE "hotwater_waterheater" DROP CONSTRAINT "hotwater_waterheater_sensor_out_id_ce02c7c8_fk_devices_t";
ALTER TABLE "hotwater_waterheater" DROP CONSTRAINT "hotwater_waterheater_sensor_out_id_key";
CREATE INDEX "hotwater_waterheater_sensor_out_id_ce02c7c8" ON "hotwater_waterheater" ("sensor_out_id");
ALTER TABLE "hotwater_waterheater" ADD CONSTRAINT "hotwater_waterheater_sensor_out_id_ce02c7c8_fk_devices_t" FOREIGN KEY ("sensor_out_id") REFERENCES "devices_tempsensor" ("name") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
