package psql;

use DBI;

my $user = "t14253sk";
my $password = "pkvdgBNc";
my $host = "webdb";

my $dbname = $user;
my $port = 5432;
my $dsn = "dbi:Pg:dbname=$dbname;host=$host;port=$port";

sub dberror{
    print $_[0];
    die;
}

sub connect{
    my $db = DBI->connect($dsn, $user, $password) or dberror(DBI::errstr);
    return $db;
}

1;
