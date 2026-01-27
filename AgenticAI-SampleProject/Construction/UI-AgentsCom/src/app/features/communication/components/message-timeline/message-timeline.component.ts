import { Component, Input, OnChanges, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { ConversationMessage } from '../../../../core/models/conversation.model';
import * as d3 from 'd3';

interface TimelineEvent {
  timestamp: Date;
  type: string;
  from: string;
  to: string;
  cycle?: number;
}

@Component({
  selector: 'app-message-timeline',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  template: `
    <mat-card class="timeline-card">
      <mat-card-header>
        <mat-card-title>Message Timeline</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div #timeline class="timeline-container"></div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .timeline-card {
      height: 100%;
    }

    mat-card-header {
      margin-bottom: 8px;
    }

    mat-card-title {
      font-size: 16px !important;
      margin: 0 !important;
    }

    .timeline-container {
      width: 100%;
      height: 200px;
      overflow-x: auto;
    }

    :host ::ng-deep {
      .timeline-event {
        cursor: pointer;
        transition: all 0.2s;

        &:hover {
          opacity: 0.8;
        }
      }

      .event-connected { fill: #4CAF50; }
      .event-request { fill: #2196F3; }
      .event-response { fill: #FF9800; }
      .event-analysis { fill: #9C27B0; }

      .cycle-marker {
        stroke: #666;
        stroke-width: 2;
        stroke-dasharray: 5,5;
      }

      .axis text {
        font-size: 11px;
      }
    }
  `]
})
export class MessageTimelineComponent implements OnChanges, AfterViewInit {
  @Input() messages: ConversationMessage[] = [];
  @ViewChild('timeline') timelineRef!: ElementRef;
  
  private svg: any;
  private initialized = false;

  ngAfterViewInit(): void {
    this.initialized = true;
    this.renderTimeline();
  }

  ngOnChanges(): void {
    if (this.initialized) {
      this.renderTimeline();
    }
  }

  private renderTimeline(): void {
    if (!this.timelineRef || this.messages.length === 0) return;

    const container = this.timelineRef.nativeElement;
    d3.select(container).selectAll('*').remove();

    const events: TimelineEvent[] = this.messages.map(m => ({
      timestamp: new Date(m.timestamp),
      type: m.type.toLowerCase(),
      from: m.from_agent,
      to: m.to_agent,
      cycle: this.extractCycle(m.content)
    }));

    const margin = { top: 20, right: 20, bottom: 40, left: 50 };
    const width = Math.max(800, events.length * 60);
    const height = 200 - margin.top - margin.bottom;

    this.svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', 200);

    const g = this.svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const xScale = d3.scaleTime()
      .domain(d3.extent(events, d => d.timestamp) as [Date, Date])
      .range([0, width - margin.left - margin.right]);

    const xAxis = d3.axisBottom(xScale)
      .ticks(5)
      .tickFormat(d3.timeFormat('%H:%M:%S') as any);

    g.append('g')
      .attr('class', 'axis')
      .attr('transform', `translate(0,${height})`)
      .call(xAxis);

    // Draw cycle markers
    const cycles = [...new Set(events.filter(e => e.cycle).map(e => e.cycle))];
    cycles.forEach(cycle => {
      const cycleEvents = events.filter(e => e.cycle === cycle);
      if (cycleEvents.length > 0) {
        const x = xScale(cycleEvents[0].timestamp);
        g.append('line')
          .attr('class', 'cycle-marker')
          .attr('x1', x)
          .attr('x2', x)
          .attr('y1', 0)
          .attr('y2', height);

        g.append('text')
          .attr('x', x)
          .attr('y', -5)
          .attr('text-anchor', 'middle')
          .attr('font-size', '10px')
          .attr('fill', '#666')
          .text(`Cycle ${cycle}`);
      }
    });

    // Draw events
    g.selectAll('.timeline-event')
      .data(events)
      .enter()
      .append('circle')
      .attr('class', (d: TimelineEvent) => `timeline-event event-${d.type}`)
      .attr('cx', (d: TimelineEvent) => xScale(d.timestamp))
      .attr('cy', height / 2)
      .attr('r', 6)
      .append('title')
      .text((d: TimelineEvent) => `${d.type.toUpperCase()}\n${d.from} → ${d.to}\n${d.timestamp.toLocaleTimeString()}`);
  }

  private extractCycle(content: string): number | undefined {
    const match = content.match(/CYCLE (\d+)/);
    return match ? parseInt(match[1]) : undefined;
  }
}
