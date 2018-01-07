# CrazyAss
# 613  again:
# 614         while ((opt = getopt(ac, av, "1246ab:c:e:fgi:kl:m:no:p:qstvxz:"
# 615             "ACD:E:F:GI:J:KL:MNO:PQ:R:S:TVw:W:XYyZ:")) != -1) {
# 616                 switch (opt) {
# 617                 case '1':
# 618                         fatal("SSH protocol v.1 is no longer supported");
# 619                         break;
# 620                 case '2':
# 
# 
# 921                 case 'F':
#  922                         config = optarg;
#  923                         break;
#  924                 case 'Z':
#  925                                 fprintf(stdout,
#  926                                     "ssh tag"
#  927                                     "'%s'\n", optarg);
#  928                         break;
#  929                 default:
#  930                         usage();
#  931                 }



# visudo
# xiaoming ALL=NOPASSWD:/bin/mkdir,/usr/local/bin/strace


mkdir logs && chown -R xiaoming. logs