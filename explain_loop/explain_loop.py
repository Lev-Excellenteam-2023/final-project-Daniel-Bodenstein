import asyncio
import signal
import sys
import logging
import explain_for_loop

logging.basicConfig(level=logging.INFO)

# Define a flag to indicate if the loop should continue running
running = True


def signal_handler(signal, frame):
    """
    Signal handler function to handle termination signal (CTRL+C).
    Sets the 'running' flag to False to stop the loop.
    """
    global running
    running = False
    logging.info("Termination signal received. Stopping the loop.")


signal.signal(signal.SIGINT, signal_handler)


async def run_loop():
    """
    Asynchronous function to run the main loop.
    """
    while running:
        logging.info('Running...')
        await explain_for_loop.explain_new_presentation()

        await asyncio.sleep(10)

    logging.info('Loop stopped.')
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(run_loop())