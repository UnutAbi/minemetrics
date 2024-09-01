import threading
import gc
from managers.classes import TimeBlock

# Global set for the resource blocks
packages: set = set()
total_time_block: TimeBlock = TimeBlock(0,0,0)

essentiel_data: dict = dict()

def post_essentiel_data(analyse_btn, analyse_btn_command, total_time_label):
    global essentiel_data

    essentiel_data["analyse_btn"] = analyse_btn
    essentiel_data["analyse_btn_command"] = analyse_btn_command
    essentiel_data["total_time_label"] = total_time_label
    

def run():
    print(f"Total Resource Blocks: {len(packages)}")

    # Start background thread for processing
    processing_thread = threading.Thread(target=process_packages)
    processing_thread.start()

def process_packages():
    global total_time_block 
    total_time_block.reset()

    from managers.mc import get_time_from_log
    from pathlib import Path

    for resource_block in packages:
        total_instances = len(resource_block.instances)
        processed_instances = 0
        resource_block_time_block = TimeBlock()  # Initialize TimeBlock for the entire resource_block
        
        for instance in resource_block.instances:
            total_logs = len(instance.logs)
            processed_logs = 0
            
            instance_time_block = TimeBlock()  # Initialize TimeBlock for the instance
                        
            for log in instance.logs:
                log_path: Path

                if Path(instance.path, "logs").exists():
                    log_path = Path(instance.path, "logs")
                else:
                    log_path = Path(instance.path)

                # Calculate log time and add to instance time block
                log_time_block: TimeBlock = get_time_from_log(Path(log_path, log))
                if log_time_block:
                    instance_time_block.add_time(log_time_block.hours, log_time_block.minutes, log_time_block.seconds)
                
                # Progress update for logs
                processed_logs += 1
                update_log_progress_label(instance, processed_logs, total_logs, instance_time_block)

            # Combine the time of the instance with the total time block of the resource_block
            resource_block_time_block.add_time(instance_time_block.hours, instance_time_block.minutes, instance_time_block.seconds)
            total_time_block.add_time(instance_time_block.hours, instance_time_block.minutes, instance_time_block.seconds)
            
            # Update gui
            update_total_time_label()

            # Change the GUI element of the instance and display the total time processed
            if "instance_status_label" in instance.gui:
                instance.gui["instance_status_label"].configure(
                    text=f"Processed {total_logs} Logs - {instance_time_block}"
                )
            
            # Update the progress of the instances in the resource_block
            processed_instances += 1
            update_progress_label(resource_block, processed_instances, total_instances, resource_block_time_block, instance)

        # After all instances for this resource_block have been processed, release memory
        gc.collect()  # Call garbage collector explicitly

    re_enable_btn_dashboard_to_scan()

def update_log_progress_label(instance, processed, total, time_block: TimeBlock):
    if "instance_status_label" in instance.gui:
        # Update the status label with the current log progress and accumulated time
        instance.gui["instance_status_label"].configure(
            text=f"Log Progress: {processed}/{total} Logs - {time_block}"
        )

def update_progress_label(resource_block, processed, total, time_block: TimeBlock, current_instance):
    if resource_block.progress_label:
        # Update the progress label with the instance progress and combined log time for the entire resource block
        if resource_block.type_label.cget("text") == "Container":
            # Wenn es sich um einen Container handelt, zeigen wir Instanzenfortschritt an
            resource_block.progress_label.configure(
                text=f"Processed {processed}/{total} Instances - {time_block}"
            )
        else:
            # Wenn es sich um eine Instanz handelt, zeigen wir Logs-Fortschritt an
            logs_count = len(current_instance.logs)
            resource_block.progress_label.configure(
                text=f"Processed {logs_count} Logs - {time_block}"
            )

def update_total_time_label():
    # Update the total gameplay time label with the accumulated time for all resource blocks
    if essentiel_data["total_time_label"]:
        essentiel_data["total_time_label"].configure(
            text=f"Total Playtime: {total_time_block}"
        )

def re_enable_btn_dashboard_to_scan():
    # Re-enable the "Start Analysis Again" button in the dashboard
    if essentiel_data["analyse_btn"]:
        essentiel_data["analyse_btn"].configure(text="Start Analysis Again", state="normal", command=essentiel_data["analyse_btn_command"], fg_color="#4DB848")
        