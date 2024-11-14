import csv
import os, sys
import json
import argparse
import sqlite3
import multiprocessing as mp
from func_timeout import func_timeout, FunctionTimedOut
import math
import numpy as np
import time


def load_json(dir):
    with open(dir, "r") as j:
        contents = json.loads(j.read())
    return contents


def result_callback(result):
    exec_result.append(result)


def execute_sql(predicted_sql, ground_truth, db_path, gt_tied_sql=""):
    conn = sqlite3.connect(db_path)
    # Connect to the database
    cursor = conn.cursor()
    cursor.execute(predicted_sql)
    predicted_res = cursor.fetchall()
    cursor.execute(ground_truth)
    ground_truth_res = cursor.fetchall()
    res = 0
    if set(predicted_res) == set(ground_truth_res):
        res = 1
    if res == 0 and gt_tied_sql != "":
        return execute_sql(predicted_sql, gt_tied_sql, db_path, "")
    return res

def execute_sqls(predicted_sqls, ground_truth, db_path, gt_tied_sql=""):
    conn = sqlite3.connect(db_path)
    # Connect to the database
    cursor = conn.cursor()
    results = list()
    for predicted_sql in predicted_sqls:
        try:
            cursor.execute(predicted_sql)
            predicted_res = cursor.fetchall()
            cursor.execute(ground_truth)
            ground_truth_res = cursor.fetchall()
            if set(predicted_res) == set(ground_truth_res):
                res = 1
            if res == 0 and gt_tied_sql != "":
                res = execute_sql(predicted_sql, gt_tied_sql, db_path, "")[0]
            results.append(res)
        except sqlite3.Warning:
            results.append(0)
        except sqlite3.Error:
            results.append(0)
    return results


def execute_model(predicted_sql, ground_truth, db_place, idx, meta_time_out, gt_tied_sql=""):
    
    try:
        if isinstance(predicted_sql, list):
            res = func_timeout(
                    meta_time_out * len(predicted_sql), execute_sqls, args=(predicted_sql, ground_truth, db_place, gt_tied_sql)
                )
        else:
            res = func_timeout(
                    meta_time_out, execute_sql, args=(predicted_sql, ground_truth, db_place, gt_tied_sql)
                )
    except KeyboardInterrupt:
        sys.exit(0)
    except FunctionTimedOut:
        res = [0] * len(predicted_sql) if isinstance(predicted_sql, list) else [0]
    except Exception as e:
        res = [0] * len(predicted_sql) if isinstance(predicted_sql, list) else [0]
    result = {
        "sql_idx": idx,
        "res": res,
    }
    return result


def package_sqls(sql_path, db_root_path, multi_sqls=False):
    clean_sqls = []
    db_path_list = []
    if multi_sqls:
        with open(sql_path, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader, None)
            for row in csv_reader:
                candidates = [r.strip() for r in row]
                clean_sqls.append(candidates)
        clean_sqls = np.array(clean_sqls).T.tolist()
    else:
        with open(sql_path) as f:
            for l in f.readlines():
                clean_sqls.append(l.strip())
                sql, db_name = clean_sqls[-1].split("\t")
                db_path_list.append(db_root_path + db_name + "/" + db_name + ".sqlite")

    return clean_sqls, db_path_list


def run_sqls_parallel(sqls, db_places, num_cpus=1, meta_time_out=30.0, gt_tied_queries=None):
    pool = mp.Pool(processes=num_cpus)
    for i, sql_pair in enumerate(sqls):
        predicted_sql, ground_truth = sql_pair
        gt_tied_sql = ""
        if gt_tied_queries:
            gt_tied_sql = gt_tied_queries[i] if i in gt_tied_queries else ""
        
        for sql in predicted_sql:
            pool.apply_async(
                execute_model,
                args=(sql, ground_truth, db_places[i], i, meta_time_out, gt_tied_sql),
                callback=result_callback,
            )
    pool.close()
    pool.join()

def sort_results(list_of_dicts):
    return sorted(list_of_dicts, key=lambda x: x["sql_idx"])

def merge_results(list_of_dicts):
    candidates = list()
    current_idx = 0
    new_list_of_dicts = list()
    for d in list_of_dicts:
        if d['sql_idx'] != current_idx:
            new_list_of_dicts.append({'sql_idx': current_idx,
                                      'res': candidates})
            candidates = list()
            current_idx = d['sql_idx']
        else:
            candidates.append(d['res'])
    if candidates:
        new_list_of_dicts.append({'sql_idx': current_idx,
                                      'res': candidates})
    return new_list_of_dicts


def compute_acc_with_candidates(exec_results, metric):
    assert metric == "res"
    num_queries = len(exec_results)
    num_candidates = len(exec_results[0][metric])

    average_acc = 0.
    for i in range(num_candidates):
        average_acc += sum([res[metric][i] for res in exec_results]) / num_queries
    average_acc /= num_candidates
    upper_acc = 0.
    lower_acc = 0.
    for i in range(num_queries):
        upper_acc += int(np.any(exec_results[i][metric] == 1))
        lower_acc += int(np.all(exec_results[i][metric] == 1))
    upper_acc /= num_queries
    lower_acc /= num_queries
    
    count_lists = [num_queries, num_queries, num_queries]
    return (
            average_acc * 100,
            upper_acc * 100,
            lower_acc * 100,
            count_lists,
        )


def print_data(score_lists, count_lists, metric="Exec ACCURACY"):
    levels = ["average", "upper bound", "lower bound"]
    print("{:20} {:20} {:20} {:20}".format("", *levels))
    print("{:20} {:<20} {:<20} {:<20}".format("count", *count_lists))

    print(
        f"====================================== {metric} ====================================="
    )
    print(
        "{:20} {:<20.2f} {:<20.2f} {:<20.2f}".format("accuracy", *score_lists)
    )


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--ground_truth_path", type=str, default=""
    )
    args_parser.add_argument(
        "--db_root_path",
        type=str,
        default="",
    )
    args_parser.add_argument("--num_cpus", type=int, default=20)
    args_parser.add_argument("--meta_time_out", type=float, default=30.0)
    args_parser.add_argument(
        "--etype",
        dest="etype",
        type=str,
        default="exec",
        choices=("exec"),
    )
    args_parser.add_argument("--gt_tied_json_path", type=str, default="")

    # input & output filse in csv format
    args_parser.add_argument("--sql_candidates_path", type=str, default="")
    args_parser.add_argument("--sql_candidates_with_label_path", type=str, default="")
    args = args_parser.parse_args()
    assert args.sql_candidates_with_label_path != "", "must specify the output path"
    exec_result = []

    assert args.sql_candidates_path
    pred_queries, db_paths = package_sqls(
        args.sql_candidates_path,
        args.db_root_path,
        multi_sqls=True,
    )
    
    # generate gt sqls:
    gt_queries, db_paths_gt = package_sqls(
        args.ground_truth_path, args.db_root_path, multi_sqls=False
    )
    # generate gt_tied sqls dict
    gt_tied_queries = {}
    if args.gt_tied_json_path:
      with open(args.gt_tied_json_path, 'r') as f:
          for tied_item in json.load(f):
              gt_tied_queries[tied_item["question_id"]] = tied_item["SQL"]

    if len(db_paths) == 0:
        db_paths = db_paths_gt

    query_pairs = list(zip(pred_queries, gt_queries))
    if args.etype in ["exec"]:
        run_sqls_parallel(
            query_pairs,
            db_places=db_paths,
            num_cpus=args.num_cpus,
            meta_time_out=args.meta_time_out,
            gt_tied_queries=gt_tied_queries,
        )
    else:
        raise NotImplementedError(f"--etype: {args.etype} is not supported")
    exec_result = sort_results(exec_result)
    exec_result = merge_results(exec_result)

    with open(args.sql_candidates_with_label_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(exec_result)

    print("start calculate")
    if args.etype in ["exec"]:
        (
            avg_acc,
            upper_acc,
            lower_acc,
            count_lists,
        ) = compute_acc_with_candidates(exec_result, "res")
        score_lists = [avg_acc, upper_acc, lower_acc]
        print_data(score_lists, count_lists, metric="Exec Accuracy")
    print(
        "==========================================================================================="
    )
    print("Finished evaluation")
