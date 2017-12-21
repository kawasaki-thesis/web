#!/usr/bin/perl
use CGI;
use psql;

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
      $cgi->start_html(-title=>'Heritage Corpus Test', -lang=>'ja-JP');

my $conn = psql->connect;

my $query = $conn->quote($cgi->param('title'));
if (length($cgi->param('title')) > 0) {
    $sql = $sql = "SELECT heritage.name, heritage.area, inner_product(heritage.c1, heritage.c2, heritage.c3, heritage.c4, heritage.c5, heritage.c6, heritage.c7, heritage.c8, heritage.c9, heritage.c10, heritage_corpus.c1,heritage_corpus.c2, heritage_corpus.c3, heritage_corpus.c4, heritage_corpus.c5, heritage_corpus.c6, heritage_corpus.c7, heritage_corpus.c8, heritage_corpus.c9, heritage_corpus.c10) AS score FROM heritage, heritage_corpus WHERE heritage_corpus.word = $query ORDER BY score DESC;";
} else {
    $sql = "SELECT heritage.name, 0 AS score FROM heritage;";
}

my $sth = $conn->prepare($sql);
my $ref = $sth->execute;

$rank=1;
print $cgi->h2('Heritage Corpus Test'),
      $cgi->p($cgi->escapeHTML($query));
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
print $cgi->end_html;

$sth->finish;
$conn->disconnect;

exit;
