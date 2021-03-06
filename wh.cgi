#!/usr/bin/perl
use CGI;
use psql;

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
      $cgi->start_html(-title=>'Recommended World Heritage List', -lang=>'ja-JP');

my $conn = psql->connect;

my $query = $cgi->param('words');
if (length($cgi->param('words')) > 0) {
    	@list = split(/,/, $query);
	foreach(@list){
		$_ =~ s/^ *(.*?) *$/$1/;
		$str = $str . 'word = \'' . $_ . '\' OR ';
	}
    chop($str);
    chop($str);
    chop($str);
    $sql = "CREATE TEMP VIEW tmpview AS SELECT c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 FROM heritage_corpus WHERE $str ; 
            CREATE TEMP VIEW sumview AS SELECT sum(c1) AS c1, sum(c2) AS c2, sum(c3) AS c3, sum(c4) AS c4,sum(c5) AS c5,sum(c6) AS c6,sum(c7) AS c7,sum(c8) AS c8,sum(c9) AS c9,sum(c10) AS c10 FROM tmpview; 
            SELECT world_heritage.name, world_heritage.country, world_heritage.area, world_heritage.img_url, world_heritage.description, world_heritage.longitude, world_heritage.latitude, 
                   inner_product(world_heritage.c1, world_heritage.c2, world_heritage.c3, world_heritage.c4, world_heritage.c5, world_heritage.c6, world_heritage.c7, world_heritage.c8, world_heritage.c9, world_heritage.c10, sumview.c1, sumview.c2, sumview.c3, sumview.c4, sumview.c5, sumview.c6, sumview.c7,sumview.c8, sumview.c9, sumview.c10) 
                   AS score 
            FROM world_heritage, sumview 
            WHERE inner_product(world_heritage.c1, world_heritage.c2, world_heritage.c3, world_heritage.c4, world_heritage.c5, world_heritage.c6, world_heritage.c7, world_heritage.c8, world_heritage.c9, world_heritage.c10, sumview.c1, sumview.c2, sumview.c3, sumview.c4, sumview.c5, sumview.c6, sumview.c7,sumview.c8, sumview.c9, sumview.c10)>0 
            ORDER BY score DESC;";
} else {
    $sql = "SELECT world_heritage.name, world_heritage.country, world_heritage.area, world_heritage.img_url, world_heritage.description, world_heritage.longitude, world_heritage.latitude, 0 AS score FROM world_heritage;";
}

my $sth = $conn->prepare($sql);
my $ref = $sth->execute;

$rank=0;
$num=1;
$num2=0;
$pre_score = 0;
print $cgi->h2('Recommended World Heritage List');
while(my $arr_ref = $sth->fetchrow_arrayref){
    my ($name, $country, $area, $url, $description, $lo, $la, $score) = @$arr_ref;
    if ($description =~ /<\/*p>/){
		$description =~ s/<\/*p>//g;
    }
    my $text = $cgi->escapeHTML("($num) $name");
    my $text2 = $cgi->escapeHTML("$country");
    my $text3 = $name . "\n" . $lo . '/' . $la . "\n" . $description;
    my $img  = $cgi->img({width=>80, src=>$url, title=>$text3});
    $sc[$rank] = $score;
    if($pre_score > $score){
              $rank++;
              $num2=0;
    }
    $table[$rank][0][$num2]=$text;
    $table[$rank][1][$num2]=$text2;
    $table[$rank][2][$num2]=$img;
    $num++;
    $num2++;
    $pre_score = $score;
}
$i=0;
foreach $ranking (@table){
	print $cgi->h3("RANK:" . ($i+1));
	print $cgi->p("Score:" . $sc[$i]);
	print '<table border="1" rules="all" valign="top">';
	foreach $tr (@{$ranking}){
		print '<tr><td valign="top">' . join('</td><td valign="top">', @{$tr}) . "</tr>";
	}
	print "</table>";
	$i++;
	$tr_count=0;
}
print $cgi->span("------------------------------"),
      $cgi->p($cgi->escapeHTML($sql)),
      $cgi->end_html;

$sth->finish;
$conn->disconnect;

exit;
