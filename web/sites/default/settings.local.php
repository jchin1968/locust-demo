<?php

# Basics
$settings['hash_salt'] = 'FdpLgwIhGuHrdAHi0D3l2Pa2PUqz3Sx7vidO505Rc_eUupcwsSCp2K59DSTKrRgNHm3tAzYByg';
$settings["config_sync_directory"] = '../config/sync';

# Database
$databases['default']['default'] = array (
  'database' => 'drupal10',
  'username' => 'drupal10',
  'password' => 'drupal10',
  'prefix' => '',
  'host' => 'database',
  'port' => '3306',
  'isolation_level' => 'READ COMMITTED',
  'driver' => 'mysql',
  'namespace' => 'Drupal\\mysql\\Driver\\Database\\mysql',
  'autoload' => 'core/modules/mysql/src/Driver/Database/mysql/',
);

# Trusted host patterns
$settings['trusted_host_patterns'] = [
  '^umami\.lndo\.site$',
];

