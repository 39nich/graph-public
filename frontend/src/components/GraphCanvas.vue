<template>
    <div id="graph-display" aria-label="generated graph">
        <canvas 
          ref="canvasRef"
          aria-label="Graph canvas with uploaded graph data" 
          style="width: 100%; height: auto; border: 1px solid #ccc;"
          @mousemove="handleHover"
          @touchmove.prevent="handleTouch"
          @touchend="handleTouchEnd"
          @touchcancel="handleTouchEnd">
        </canvas>
    </div>
	<label
	ref="hapticLabel"
	aria-hidden="true"
 	style="
    position: absolute;
    width: 50px;
    height: 30px;
    top: -1000px;
    left: -1000px;
    opacity: 0;
    pointer-events: none;
    display: inline-block;
  "
>
  <input
    ref="hapticCheckbox"
    type="checkbox"
	role="switch"
	aria-hidden="true"
    style="
      width: 100%;
      height: 100%;
      appearance: none;
      -webkit-appearance: none;
      background: #ccc;
      border-radius: 15px;
      position: relative;
    "
  />
</label>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useGraphStore } from '@/stores/graph'
import { nextTick } from 'vue'
import { distanceToSegment, getBounds, normalize } from '@/utils/graphUtils'

const store = useGraphStore()
const canvasRef = ref<HTMLCanvasElement | null>(null)
const normalizedPoints = ref<{ x: number, y: number, original: number[] }[]>([])

const hapticLabel = ref<HTMLLabelElement | null>(null);
const hapticCheckbox = ref<HTMLInputElement | null>(null);

class AudioManager {
	private audioContext: AudioContext | null = null;
	private beepIntervalId: number | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
  }

  startRepeatingBeep(frequency: number, beepDuration: number, totalCycle: number) {
    if (!this.audioContext) return;

    if (this.beepIntervalId !== null) return;

    const playSingleBeep = () => {
      if (this.audioContext!.state === 'suspended') {
        this.audioContext!.resume();
      }

      const oscillator = this.audioContext!.createOscillator();
      const gainNode = this.audioContext!.createGain();

      oscillator.type = 'triangle'; 
      oscillator.frequency.setValueAtTime(frequency, this.audioContext!.currentTime);

      oscillator.connect(gainNode);
      gainNode.connect(this.audioContext!.destination);

      oscillator.start();

      setTimeout(() => {
        oscillator.stop();
        oscillator.disconnect();
        gainNode.disconnect();
      }, beepDuration);
    };

    // Start immediately    
    playSingleBeep();

    // Repeat
    this.beepIntervalId = window.setInterval(playSingleBeep, totalCycle);
  }

  stopRepeatingBeep() {
    if (this.beepIntervalId !== null) {
      clearInterval(this.beepIntervalId);
      this.beepIntervalId = null;
    }
  }
}

// --- Instantiate AudioManager ---
const audioManager = new AudioManager();

class VibrationManager {
	private intervalId: number | null = null;

	start(pattern: number[] = [500, 500]) {
		if (!('vibrate' in navigator)) return;

		if(this.intervalId !== null) return;

		navigator.vibrate(pattern);

		const cycleDuration = pattern.reduce((a,b) => a + b, 0);
		this.intervalId = window.setInterval(() => {
			navigator.vibrate(pattern);
		}, cycleDuration);
	}

	stop() {
		if (!('vibrate' in navigator)) return;

		navigator.vibrate(0); // Immediately stop vibration
		if (this.intervalId !== null) {
		clearInterval(this.intervalId);
		this.intervalId = null;
		}
	}
}

const vibrate = new VibrationManager();

function handleGraphInteraction(activate: boolean) {
  if (activate) {
	vibrate.start();
	audioManager.startRepeatingBeep(500, 200, 500);
  } else {
	vibrate.stop();
    audioManager.stopRepeatingBeep();
  }
}

// const canUseVibrate = typeof navigator !== "undefined" && "vibrate" in navigator;
// const vibrate = debounce(() => {
//   if (canUseVibrate) {
//     // Android (or devices that support navigator.vibrate)
//     navigator.vibrate(50); // Vibrate for 50ms
//   } else if (hapticCheckbox.value) {
//     // iOS fallback: simulate a vibration by toggling the checkbox
//     hapticLabel.value?.click();
//   }
// }, 100); // 100ms debounce

watch(
  () => store.graphData?.coord_data,
  async (newData) => {
    if (!newData || newData.length === 0) {
      console.log("coord_data is empty!")
      return
    }

    await nextTick() // wait for canvas to be in the DOM

    if (!canvasRef.value) {
      console.log("Canvas still not ready!")
      return
    }

    const canvas = canvasRef.value
    
	if (canvas) {
      const parent = canvas.parentElement

      if (parent) {
        canvas.width = parent.clientWidth
        canvas.height = window.innerHeight - parent.getBoundingClientRect().top - 40 
      }
	}
    console.log("Canvas size:", canvas.width, canvas.height)

    const coordArray = newData as [number, number][]
    const { xMin, xMax, yMin, yMax } = getBounds(coordArray)
    console.log("Bounds:", { xMin, xMax, yMin, yMax })

    normalizedPoints.value = coordArray.map(([x, y]) => {
      const [nx, ny] = normalize(x, xMin, xMax, y, yMin, yMax, canvas.width, canvas.height)
      return { x: nx, y: ny, original: [x, y] }
    })

    console.log("Normalized points:", normalizedPoints.value.slice(0, 5))
    drawGraph()
  },
  { immediate: true }
)


function drawGraph() {
  console.log("drawGraph() called with", normalizedPoints.value.length, "points")
  if (!canvasRef.value || normalizedPoints.value.length === 0) return

  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  if(!ctx) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.beginPath() 

  normalizedPoints.value.forEach(({ x, y }, i) => {
      if (i === 0) ctx.moveTo(x,y)

      else ctx.lineTo(x,y)
  })

  ctx.strokeStyle = 'blue'
  ctx.lineWidth = 2
  ctx.stroke()

  for (const {x, y} of normalizedPoints.value) {
      ctx.beginPath()
      ctx.arc(x, y, 5, 0, Math.PI*2)
      ctx.fillStyle = 'blue'
      ctx.fill()
  }
}


let graphHoverActive = false
let hoverTimeout: number | null = null;

function handleHover(event: MouseEvent) {
    if (!canvasRef.value) return;

    const rect = canvasRef.value.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const threshold = 15; // pixels
    const points = normalizedPoints.value;

    for (let i = 0; i < points.length - 1; i++) {
        const p1 = points[i];
        const p2 = points[i + 1];

        const dist = distanceToSegment(x, y, p1.x, p1.y, p2.x, p2.y);

        if (dist < threshold) {
            console.log(`Hover near line segment between: (${p1.original[0]}, ${p1.original[1]}) and (${p2.original[0]}, ${p2.original[1]})`);
            
			if(!graphHoverActive) {
				graphHoverActive = true;
				handleGraphInteraction(true);
				console.log("Activated")
			}
			if(hoverTimeout) {
				clearTimeout(hoverTimeout);
				hoverTimeout = null;
			}
            
			return;
        }
    }
    if (hoverTimeout == null) {
        hoverTimeout = window.setTimeout(() => {
            console.log("Not near any segment");
            graphHoverActive = false;
            handleGraphInteraction(false);	
            hoverTimeout = null;
        }, 100);
    }
}

let graphTouchActive = false
let touchTimeout: number | null = null;
function handleTouch(event: TouchEvent) {
    if (!canvasRef.value) return
    const rect = canvasRef.value.getBoundingClientRect()
    const touch = event.touches[0]
    const x = touch.clientX - rect.left
    const y = touch.clientY - rect.top

    const threshold = 15;
    const points = normalizedPoints.value;
	
    for (let i = 0; i < points.length - 1; i++) {
        const p1 = points[i];
        const p2 = points[i + 1];

        const dist = distanceToSegment(x, y, p1.x, p1.y, p2.x, p2.y);
		
        if (dist < threshold) {
			console.log(`Touch near line segment between: (${p1.original[0]}, ${p1.original[1]}) and (${p2.original[0]}, ${p2.original[1]})`);
			
			if(!graphTouchActive) {
				graphTouchActive = true;
				handleGraphInteraction(true);
			}
			if(touchTimeout) {
				clearTimeout(touchTimeout);
				touchTimeout = null;
			}
			return;
		}
	}
	if(touchTimeout == null) {
		touchTimeout = window.setTimeout(() => {
			console.log("Not near any segment");
			graphTouchActive = false;
			handleGraphInteraction(false);
			touchTimeout = null;
		}, 100);
	}

}

function handleTouchEnd() {
	graphTouchActive = false;
	handleGraphInteraction(false);
}

</script>

<style scoped>
#graph-display {
	width: 100%;
	margin: 1rem auto;
}
</style>