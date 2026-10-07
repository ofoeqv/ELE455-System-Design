"""Run the AES preparation exercises with Verilator; no Makefile to write."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['week1', 'week2', 'shared', 'parallel'])
    parser.add_argument('--bench', choices=['cocotb', 'verilog'], default='cocotb')
    parser.add_argument('--rtl-dir', type=Path, default=ROOT,
                        help='Staff only: directory containing completed RTL')
    parser.add_argument('--build-root', type=Path, default=ROOT.parent/'build'/'preparation')
    args = parser.parse_args()

    top = {'week1':'byte_key_xor', 'week2':'byte_transform',
           'shared':'state_transform', 'parallel':'state_transform'}[args.target]
    lanes = 4 if args.target == 'shared' else 16
    width = 128 if args.target in ('shared', 'parallel') else 8
    latency = 4 if args.target == 'shared' else 1
    build = (args.build_root/(args.target+'_'+args.bench)).resolve()
    build.mkdir(parents=True, exist_ok=True)
    rtl = args.rtl_dir.resolve()/f'{top}.v'
    parameters = {'LANES':lanes} if width == 128 else {}

    if args.bench == 'verilog':
        tb = 'tb_byte_key_xor' if args.target == 'week1' else 'tb_transform'
        command = ['verilator', '--binary', '--timing', '--top-module', tb,
                   '--Mdir', str(build), '-o', 'simulation', str(rtl), str(ROOT/f'{tb}.v')]
        if args.target != 'week1':
            command += [f'-DDUT={top}', f'-GWIDTH={width}', f'-GLATENCY={latency}']
        if width == 128:
            command += ['-DSTATE_DUT', f'-GLANES={lanes}']
        subprocess.run(command, check=True, timeout=180)
        result = subprocess.run([str(build/'simulation')], check=False,
                                capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        result.check_returncode()
        assert 'PASS preparation' in result.stdout
        return

    from cocotb_tools.runner import get_runner
    module = 'test_byte_key_xor' if args.target == 'week1' else 'test_transform'
    sys.path.insert(0, str(ROOT))
    result_path = build/'results.xml'
    if result_path.exists():
        result_path.unlink()
    runner = get_runner('verilator')
    runner.build(sources=[rtl], hdl_toplevel=top, build_dir=build,
                 parameters=parameters, always=True)
    runner.test(hdl_toplevel=top, test_module=module, test_dir=build,
                results_xml=str(result_path), extra_env={
                    'PYTHONPATH':str(ROOT)+os.pathsep+os.environ.get('PYTHONPATH',''),
                    'PREP_WIDTH':str(width), 'PREP_LATENCY':str(latency)})
    tree = ET.parse(result_path)
    assert list(tree.iter('testcase')), 'No tests executed'
    assert not any(list(tree.iter(tag)) for tag in ('failure','error','skipped'))
    print('PASS preparation', args.target, args.bench)

if __name__ == '__main__':
    main()
