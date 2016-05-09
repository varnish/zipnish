CREATE DATABASE  IF NOT EXISTS `microservice` DEFAULT CHARSET=utf8;

USE `microservice`;

-- Table structure for table 'zipnish_spans'
--

DROP TABLE IF EXISTS `zipnish_spans`;
CREATE TABLE IF NOT EXISTS `zipnish_spans` (
      `span_id` BIGINT NOT NULL,
      `parent_id` BIGINT,
      `trace_id` BIGINT NOT NULL,
      `span_name` VARCHAR(255) NOT NULL,
      `debug` SMALLINT NOT NULL,
      `duration` BIGINT,
      `created_ts` BIGINT
);

ALTER TABLE zipnish_spans ADD INDEX(`span_id`);
ALTER TABLE zipnish_spans ADD INDEX(`trace_id`);
ALTER TABLE zipnish_spans ADD INDEX(`span_name`);
ALTER TABLE zipnish_spans ADD INDEX(`created_ts`);


-- Table structure for table 'zipnish_annotations'
--
DROP TABLE IF EXISTS `zipnish_annotations`;
CREATE TABLE `zipnish_annotations` (
     `span_id` BIGINT NOT NULL,
     `trace_id` BIGINT NOT NULL,
     `span_name` VARCHAR(255) NOT NULL,
     `service_name` VARCHAR(255) NOT NULL,
     `value` TEXT,
     `ipv4` INT,
     `port` INT,
     `a_timestamp` BIGINT NOT NULL,
     `duration` BIGINT
);


ALTER TABLE zipnish_annotations ADD FOREIGN KEY(`span_id`) REFERENCES zipnish_spans(`span_id`) ON DELETE CASCADE;
ALTER TABLE zipnish_annotations ADD INDEX(`trace_id`);
ALTER TABLE zipnish_annotations ADD INDEX(`span_name`);
ALTER TABLE zipnish_annotations ADD INDEX(`a_timestamp`);