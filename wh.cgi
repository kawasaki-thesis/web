#!/usr/bin/perl
use CGI;
use psql;

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
      $cgi->start_html(-title=>'Heritage Corpus Test', -lang=>'ja-JP');

my $conn = psql->connect;

my $query = $cgi->param('words');
if (length($cgi->param('words')) > 0) {
    	@list = split(/,/, $query);
        #map{$_ =~ s/^ *(.*?) *$/$1/; $_ }@list;
        #map{$_ = 'word = \'' . $_ . '\' OR '; $_}@list;
	foreach(@list){
		$_ =~ s/^ *(.*?) *$/$1/;
		$str = $str . 'word = \'' . $_ . '\' OR ';
	}
    chop($str);
    chop($str);
    chop($str);
    $sql = "CREATE TEMP VIEW tmpview AS SELECT c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 FROM heritage_corpus WHERE $str ; CREATE TEMP VIEW sumview AS SELECT sum(c1) AS c1, sum(c2) AS c2, sum(c3) AS c3, sum(c4) AS c4,sum(c5) AS c5,sum(c6) AS c6,sum(c7) AS c7,sum(c8) AS c8,sum(c9) AS c9,sum(c10) AS c10 FROM tmpview; SELECT heritage.name, heritage.area, inner_product(heritage.c1, heritage.c2, heritage.c3, heritage.c4, heritage.c5, heritage.c6, heritage.c7, heritage.c8, heritage.c9, heritage.c10, sumview.c1, sumview.c2, sumview.c3, sumview.c4, sumview.c5, sumview.c6, sumview.c7,sumview.c8, sumview.c9, sumview.c10) AS score FROM heritage, sumview ORDER BY score DESC;";
} else {
    $sql = "SELECT heritage.name, 0 AS score FROM heritage;";
}

my $sth = $conn->prepare($sql);
my $ref = $sth->execute;

$rank=1;
print $cgi->h2('Heritage Corpus Test'),
      $cgi->p($cgi->escapeHTML($query)),;
while(my $arr_ref = $sth->fetchrow_arrayref){
    my ($name, $area, $score) = @$arr_ref;
    my $text = $cgi->escapeHTML("($rank) $name / $area");
    my $text2 = $cgi->escapeHTML("score: $score");
    print $cgi->span($text),
          $cgi->br,
          $cgi->span($text2),
          $cgi->br,
          $cgi->br;
    $rank++;
}
print $cgi->span("------------------------------"),
      $cgi->p($cgi->escapeHTML($sql)),
      $cgi->end_html;

$sth->finish;
$conn->disconnect;

exit;