 if [ "$#" -eq  "2" ]
   then
     trec_eval -q $1 -m success.1,2,3,5,10,20,25,50,75,100 -m ndcg_cut.5 -m recip_rank -m all_trec $2
 else
 	 echo "agvaluate_eval.sh runs trec_eval with:\n - success@1,2,3,5,10,20,25,50,75,100 \n - ndcg@5 \n - recip_rank \n - all_trec"
     echo "Usage: agvaluate_eval.sh trec_rel_file trec_top_file"
 fi

