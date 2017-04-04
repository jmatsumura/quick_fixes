#!/usr/bin/perl -w

=head1 NAME

delete_accesions.pl

=head1 SYNOPSIS

Marks accessions noted, one per line, in a file as obsolete within a Chado MySQL DB. 

=head1 DESCRIPTION

This script takes in six arguments, the MySQL host name, the MySQL DB name, a valid 
username, a valid password, either 'delete' or 'recover' for whether to mark these
accessions as obsolete or not, and a valid path to a file that contains accessions. 

Run it like so:

perl delete_accesions.pl mysql_host database username password (delete|recover) /path/to/file

=head1 AUTHOR - James Matsumura

e-mail: jmatsumura@som.umaryland.edu

=cut

use strict;
use DBI;

my ($host,$db,$user,$pw,$d_or_r,$file) = @ARGV;

# Make the default keep the ID as a real ID, if user chooses to delete then 
# change the value.
my $obs_val = 0; 
if ($d_or_r eq 'delete'){
	$obs_val = 1;
}

# connect to MySQL
my $dbh = DBI->connect("DBI:mysql:database=$db;host=$host",
						"$user", "$pw");

open(my $fh, $file) or die "Could not open file '$file' $!";

# Iterate over the input file and for each accession present either mark as obsolete or recover it
while (my $row = <$fh>) {
	chomp $row;
	my $acc = $row;
	my $statement = $dbh->prepare("UPDATE feature,dbxref,feature_dbxref SET feature.is_obsolete=? WHERE dbxref.accession=? AND dbxref.dbxref_id=feature_dbxref.dbxref_id AND feature_dbxref.feature_id=feature.feature_id");
	$statement->execute($obs_val,$acc);
}

$dbh->disconnect();
