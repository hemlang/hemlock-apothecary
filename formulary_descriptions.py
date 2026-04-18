"""Formulary task descriptions — one imperative phrase per stdlib seed.

Keyed by (module, task_name). Each description should describe the *problem*
without naming the stdlib module — the generator decides per-row whether to
append a "Use @stdlib/X" hint or not, so the model learns both:

  (a) when told the module, import and use it correctly
  (b) when given a problem, recognize the right module on its own

Style: Write each description as a bare imperative phrase so it slots into
"Write a Hemlock program to {desc}" and "In Hemlock, {desc}".
Example: "compute the mean of a list" (good), "computes the mean..." (wrong).

Naming convention for .hml files: hemlock/stdlib/<module>/<task>.hml
"""

DESCRIPTIONS = {
    # ---------------- math ----------------
    ("math", "sqrt_distance"):
        "compute 2D Euclidean distance for a few point pairs and print each result to 4 decimal places",
    ("math", "mean_stddev"):
        "compute the arithmetic mean and population standard deviation of a list of numbers and print each rounded to 2 decimals",
    ("math", "trig_unit_circle"):
        "print cos(a) and sin(a) at five angles around the unit circle (0, PI/4, PI/2, PI, 3PI/2), each formatted to 4 decimals",
    ("math", "compound_interest"):
        "compute compound interest on $1000 at 5% for years 1 through 5 using pow(), and print each yearly balance formatted to 2 decimals",
    ("math", "gcd_lcm_reduce"):
        "reduce a few fractions to lowest terms using gcd(), then print the lcm of two integer pairs",
    ("math", "rounding_modes"):
        "print floor, ceil, round, and trunc of a handful of positive and negative decimals so the difference between the four modes is visible",
    ("math", "clamp_bounds"):
        "clamp a list of sensor readings into the range [0, 100] and print each clamped value",
    ("math", "seeded_dice"):
        "seed the RNG to 42, roll ten six-sided dice using floor(rand_range(1.0, 7.0)), print the rolls comma-separated, and print the sum",

    # ---------------- decimal ----------------
    ("decimal", "format_currency"):
        "iterate a list of priced items, print each price formatted as USD to 2 decimals, then print the total",
    ("decimal", "int_base_convert"):
        "print a few integers in hexadecimal, octal, and binary using to_hex, to_oct, and to_bin",
    ("decimal", "parse_int_bases"):
        "parse several numeric strings using parse_int with different radixes (10, 16, 2, 8) and print each parsed value",
    ("decimal", "parse_float_sum"):
        "parse a list of numeric strings with parse_float, print each parsed value, and print the total to 4 decimals",
    ("decimal", "stringbuilder_csv"):
        "build a CSV document using StringBuilder (sb_new/sb_append/sb_to_string) and print the result",

    # ---------------- hash ----------------
    ("hash", "sha256_hex"):
        "print the SHA-256 and MD5 hex digests of the string 'hello world'",

    # ---------------- json ----------------
    ("json", "parse_roundtrip"):
        "parse a JSON user record, increment the age field, append a tag to the tags array, and print the re-serialized JSON",
    ("json", "pretty_config"):
        "parse a compact JSON config string and print it pretty-printed with 2-space indentation",
    ("json", "get_nested_paths"):
        "read several dot-path values from a nested JSON-like object using get(), including a missing path with a default",
    ("json", "set_deep_update"):
        "apply three deep updates to a parsed JSON document using set() (nested object field, array index, and a second-level field), then print the re-serialized JSON",
    ("json", "order_totals"):
        "parse a JSON array of order records and print the count, total amount, and max amount formatted to 2 decimals",
    ("json", "merge_configs"):
        "spread an overrides object over a defaults object to produce a merged configuration, then print the merged JSON",

    # ---------------- collections ----------------
    ("collections", "hashmap_word_count"):
        "count word occurrences in a space-separated string using a hash map, then print each word and its count",
    ("collections", "set_unique_tags"):
        "deduplicate a list of tags using a Set, print the sorted unique tags, and show union/intersection with a second Set",
    ("collections", "queue_print_jobs"):
        "enqueue three print jobs, peek at the front, then dequeue and print each job until the Queue is empty",
    ("collections", "stack_balanced_parens"):
        "use a Stack to check whether several bracket expressions are balanced and print true/false for each",
    ("collections", "lru_cache_access"):
        "create an LRUCache with capacity 3, insert four keys with an access pattern that evicts one, and print which keys remain",

    # ---------------- csv ----------------
    ("csv", "parse_stringify"):
        "parse a CSV string into rows, print each row joined with ' | ', then re-serialize with stringify()",
    ("csv", "parse_objects_header"):
        "parse a CSV string into an array of objects using the first row as headers, then print each record as 'name: score'",
    ("csv", "column_sum"):
        "parse a CSV and sum the values of a numeric column using get_column() and parse_int()",
    ("csv", "filter_active"):
        "parse a CSV of users into objects, filter rows where status is 'active', and re-emit them using stringify_objects()",

    # ---------------- strings ----------------
    ("strings", "case_conversions"):
        "take a few sample strings and print each converted to snake_case, camel_case, pascal_case, and kebab_case",
    ("strings", "padding_table"):
        "print a centered header and a table of names and scores using pad_right for text columns and pad_left for numeric columns",
    ("strings", "reverse_palindrome"):
        "check whether each of several words is a palindrome by lowercasing and comparing against its reverse",
    ("strings", "truncate_summary"):
        "truncate a list of article titles to 30 characters with '...' suffix and print each",
    ("strings", "lines_and_words"):
        "split a multi-line document with lines() and words(), printing each numbered line and the overall word count",

    # ---------------- datetime ----------------
    ("datetime", "format_iso"):
        "construct a specific DateTime with from_date() and print it as ISO, date, time, and two custom %-format strings",
    ("datetime", "date_arithmetic"):
        "starting from 2026-01-01, compute dates +7 days, +30 days, and +365 days using add_days, then print diff_days between first and last",
    ("datetime", "parse_iso"):
        "parse several ISO-8601 timestamps with parse_iso() and print each as 'weekday month-name time'",
    ("datetime", "weekday_lookup"):
        "given a handful of holiday dates in 2026, use from_date() and weekday_name() to print which weekday each falls on",

    # ---------------- encoding ----------------
    ("encoding", "base64_roundtrip"):
        "base64-encode and then base64-decode three sample strings and print each 'original -> encoded -> decoded' line",
    ("encoding", "hex_roundtrip"):
        "hex-encode and hex-decode a few strings and print the round-trip for each",
    ("encoding", "url_query"):
        "url-encode a list of query-parameter key/value pairs and print them joined as a single URL query string",

    # ---------------- regex ----------------
    ("regex", "email_test"):
        "use test() with REG_EXTENDED to validate a few candidate email addresses against a pattern and print true/false for each",
    ("regex", "extract_number"):
        "for each log line, use test() with REG_EXTENDED and the pattern [0-9]+ to print whether it contains any digits",

    # ---------------- yaml ----------------
    ("yaml", "parse_stringify"):
        "parse a small YAML config (server block + features list), print a few fields, then re-emit it with stringify()",
    ("yaml", "get_nested"):
        "parse a nested YAML document and read three dotted paths with get()",

    # ---------------- toml ----------------
    ("toml", "parse_stringify"):
        "parse a TOML document with a top-level key and two tables, print a summary, then re-serialize it",
    ("toml", "get_nested"):
        "parse a TOML config with a nested [app.limits] table and read four dotted paths using get()",

    # ---------------- url ----------------
    ("url", "parse_parts"):
        "parse a full URL with userinfo, port, path, query, and fragment using parse(), then print each component",
    ("url", "query_params"):
        "parse a query string with parse_query(), print each name/value, then use get_query_param and set_query_param on a full URL",
    ("url", "encode_component"):
        "round-trip several raw strings through encode_component and decode_component and print each 'raw -> encoded -> decoded' triple",

    # ---------------- uuid ----------------
    ("uuid", "validate_static"):
        "check a list of candidate UUID strings with is_valid(), and for each valid one also print is_nil() and to_upper()",
    ("uuid", "compare_equals"):
        "use equals(), compare(), and is_nil() to classify relationships between a handful of hard-coded UUID strings",

    # ---------------- fmt ----------------
    ("fmt", "printf_format"):
        "use format() with %s/%d/%.Nf/%x/%o/%b specifiers and width/flag modifiers (%10s, %-10s, %05d, %+d) to print a few lines",
    ("fmt", "thousands_bytes"):
        "format a few integers with thousands(), convert byte counts to human units with bytes_size(), and print durations and ordinals",
    ("fmt", "percent_wrap"):
        "use percent() to format ratios as percentages (default and 2-decimal precision), then use wrap() to soft-wrap a paragraph to 30 chars",

    # ---------------- path ----------------
    ("path", "join_split"):
        "use path.join to build a path, then extract directory, basename (with and without suffix), and extension",
    ("path", "normalize"):
        "normalize a handful of messy paths (redundant slashes, '..' and '.') using normalize() and also print is_absolute() for each",
    ("path", "parse_format"):
        "parse a full filesystem path into {root, dir, base, name, ext} components, print each field, and reassemble via format()",

    # ---------------- atomic ----------------
    ("atomic", "counter"):
        "allocate a 4-byte ptr as a shared counter, then use atomic_store_i32, atomic_add_i32, atomic_sub_i32, and atomic_load_i32 to mutate and print its value, free at the end",
    ("atomic", "compare_and_swap"):
        "allocate an i32 counter, initialize to 42, then demonstrate a successful and a failed atomic_cas_i32 call, printing whether each swap succeeded and the final value",

    # ---------------- async ----------------
    ("async", "parallel_map_squares"):
        "use parallel_map with a 4-worker pool to square each element of a ten-element array, then print the comma-separated squares and their sum",

    # ---------------- iter ----------------
    ("iter", "range_enumerate"):
        "use range() with one and three arguments to build two sequences, then print enumerate() pairs of a color list starting at 1",
    ("iter", "zip_unzip"):
        "zip names with ages into pairs and print each as 'name is age', then use unzip() to split them back into two parallel arrays",
    ("iter", "chunk_take"):
        "split a ten-element array into chunks of 3 with chunk() and print each group, then take() the first 5 elements",

    # ---------------- assert ----------------
    ("assert", "basic_checks"):
        "use assert, assert_eq, assert_ne, and assert_type to verify a simple add() function and a couple of type checks, then print a success message",

    # ---------------- bytes ----------------
    ("bytes", "byte_swap"):
        "byte-swap a u16, u32, and u64 using bswap16/bswap32/bswap64 and print each 'before -> after' pair in hex",
    ("bytes", "network_order"):
        "convert a u16 port and a u32 IPv4 address to network byte order with htons/htonl, then back with ntohs/ntohl, printing each step in hex",

    # ---------------- testing ----------------
    ("testing", "simple_suite"):
        "build a tiny test suite with two describe() blocks covering arithmetic and strings, using expect(x).to_equal(y), and call run() to print the report",

    # ---------------- semver ----------------
    ("semver", "parse_compare"):
        "parse three version strings into objects, print their components, then use compare() to order a few pairs",
    ("semver", "satisfies_range"):
        "check whether a list of versions satisfies the caret range '^1.2.0' and then print patch/minor/major increments of 1.2.3",

    # ---------------- compression ----------------
    ("compression", "gzip_roundtrip"):
        "gzip a repeating string, then gunzip it, printing original byte length, whether the round-trip matches, and the restored byte length",
    ("compression", "deflate_levels"):
        "deflate_compress a string at levels 1 and 9, then inflate_decompress and verify the round-trip matches the original",

    # ---------------- args ----------------
    ("args", "parse_flags"):
        "parse a synthetic argv like ['script.hml', 'build', '--verbose', '--output', 'out.txt', 'src/main.hml'] and print the flag, an option with default, and the positionals",

    # ---------------- random ----------------
    ("random", "seeded_picks"):
        "set_seed(12345) and print five randint(1,100) values, a choice from a color list, and a sample of 3",
    ("random", "seeded_shuffle"):
        "shuffle a deck [1..10] with set_seed(7), then reshuffle a fresh copy with the same seed and verify the outputs are identical",

    # ---------------- arena ----------------
    ("arena", "bump_allocator"):
        "create a 1024-byte Arena, perform three allocations (alloc, alloc, alloc_aligned), print used/capacity/remaining, reset, and destroy",
    ("arena", "save_restore"):
        "allocate one persistent block in an Arena, save() the mark, allocate two temporary blocks, then restore() and print used bytes at each step",

    # ---------------- matrix ----------------
    ("matrix", "add_multiply"):
        "build two 2x2 matrices with from_rows(), then print each row of their sum (add) and product (mul)",
    ("matrix", "transpose_identity"):
        "build a 2x3 matrix with from_rows, print its transpose row by row, then build a 3x3 identity() and print its rows",
    ("matrix", "determinant_trace"):
        "compute and print det() and trace() for a 2x2 and a 3x3 matrix constructed via from_rows()",

    # LinkedList (requires PR #519) and regex replace_all (requires PR #520)
    ("collections", "linkedlist_playlist"):
        "build a playlist in a LinkedList using append, prepend, and insert; iterate by index to print each item; print contains/index_of checks; then remove the head, reverse in place, and print the final order",
    ("collections", "to_array_pipelines"):
        "build a LinkedList, Queue, and Stack; call to_array() on each and pipe the result through array sort/map/filter/reverse, printing each transformed result",
    ("regex", "replace_whitespace"):
        "use replace_all with REG_EXTENDED to collapse runs of spaces into a single space and to replace every digit run with 'NUM', then print both results",

    # TODO: expand with 5-10 tasks per module across the 53 stdlib modules.
    # Priority fill order (based on Codex L2/L3/L5 failure patterns):
    #   1. math, decimal           (float formatting, divi, to_fixed)
    #   2. collections             (HashMap/Set/Queue/Stack APIs)
    #   3. json, csv, yaml, toml   (data parsing — caused L2 timeouts)
    #   4. strings                 (char_at, byte_at, split, replace)
    #   5. datetime, time          (common to practical tasks)
    #   6. hash, encoding, crypto  (one-liner stdlib exercises)
    #   7. async, atomic, channel  (fixes L4 concurrency misses)
    #   8. fs, path, glob, env     (scripting plumbing)
    #   9. regex, fmt, logging
    #  10. http, net, websocket, unix_socket
    #  11. process, signal, shell, os
    #  12. sqlite, mmap, arena, ffi, ipc
    #  13. remainder
}
